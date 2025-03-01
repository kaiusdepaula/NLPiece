import pandas as pd

from tqdm import tqdm
from typing import Literal
import re

onepiecedata = pd.read_parquet("outputs/OnePieceData.parquet")

# This is a way of removing "recurrently bad tokens"
recurring_phrases = onepiecedata["text"].value_counts().reset_index(name="freq")
recurring_phrases = recurring_phrases[recurring_phrases["freq"] > 3].text 

def generate_document_by_group(onepiecedata:pd.DataFrame, group_name:Literal["volume", "character"]) -> pd.DataFrame:
    """Takes the previously generated dataset and compress it to a given level."""
    grouped = onepiecedata.groupby(group_name)

    # Prepare a dictionary to collect results
    result = {}
    for id, group in tqdm(grouped, desc="Processing Texts"):
        all_values = group["text"].explode().to_list()
        all_values = [ text for text in all_values if text not in recurring_phrases ]

        # Phrases with less than 5 words are more likely to be bad tokens.
        unique_values = [ 
            re.sub('[^a-zA-Z0-9 \n\.]', '', text.lower()) 
            for text in set(all_values) 
            if len(set(text)) >= 5
        ] 
        result[id] = ". ".join([ text.replace(".", "") for text in unique_values if text != ""])

    # Convert result dictionary into a DataFrame
    data = pd.DataFrame.from_dict(result, orient='index', columns=["text"]).reset_index(names=group_name)
    return data

def generate_docs():
    """Simple main function to run for all levels the inner function."""
    
    groups = ["volume", "character"]
    for group in groups:
        volumes_data = generate_document_by_group(onepiecedata, group)
        # If group is volume, get saga labels
        if group == "volume":
            labels = onepiecedata[
                ["volume", "saga", "saga_expanded"]
            ].drop_duplicates(subset=['volume'])

            volumes_data = pd.merge(
                volumes_data,
                labels,
                how= "left",
                on= "volume"
            )
        volumes_data.to_parquet(f"outputs/{group}.parquet", index=False)

if __name__=="__main__":
    generate_docs()