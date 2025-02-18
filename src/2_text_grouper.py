import pandas as pd
from tqdm import tqdm
from utils import OnePieceSaga
one_piece = OnePieceSaga()

def get_all_volumes():
    """This script is responsible for concatenating all transcripts in a same data structure"""
    all_data = pd.DataFrame(columns=["text", "volume", "character"])

    volumes = [f"{i:03d}" for i in range(1, 105)]
    for volume in tqdm(volumes):
        data = pd.read_fwf(f"transcripts/v{volume}/transcript.txt", delimiter="\t", header=None)
        data.columns = ["text"]

        data["volume"] = int(volume)
        data["character"] = data["text"].str.extract(r"<(.*?)>")
        data["text"] = data["text"].str.replace(r"<.*?>:\s*", "", regex=True)

        all_data = pd.concat([all_data, data], axis=0)

    # Optional: filter out or standardize characters
    character_mapping = {
        "Nami Kimono": "Nami",
        "Toy Soldier (kyros)": "Kyros",
        "Luci (luffy)": "Luffy",
        "Usopp (sogeking)": "Usopp",
        "Robin (hatless)": "Robin",
        "1362633993923379712": "Other",
        "Luffy (kid)": "Luffy",
        "Kaido (dragon)": "Kaido",
        "Kaido (hybrid)": "Kaido",
        "Luffy wano": "Luffy",
        "Doflaming": "Doflamingo",
    }

    # Apply replacement
    all_data["character"] = all_data["character"].replace(character_mapping)

    # Get saga references
    all_data["saga"] = all_data["volume"].apply(lambda x: one_piece.get_saga_by_volume(x).replace("_", " "))
    all_data["saga_expanded"] = all_data["volume"].apply(lambda x: one_piece.get_extended_saga_by_volume(x).replace("_", " "))
    
    print("Finished merging all volumes together!")
    print(f"All {len(set(all_data["volume"]))} volumes have been processed.")
    print(f"There are {len(set(all_data["character"]))} different characters.")
    print(f"Dataset is {all_data.shape[0]} rows long.")
    print(f"Saving it into 'outputs/OnePieceData.parquet'")
    all_data.to_parquet("outputs/OnePieceData.parquet", index=False)

if __name__ == "__main__":
    get_all_volumes() 