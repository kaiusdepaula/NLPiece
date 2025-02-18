from transformers import AutoModel
import torch
import os
import gc
from utils import OnePieceSaga, read_image
one_piece = OnePieceSaga()

os.makedirs("outputs", exist_ok=True)
os.makedirs("outputs/magiv2", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True).cuda().eval()

def generate_transcripts():
    """
    This function is responsable for the entirety of transcript generation.
    It works byt looking for each defined saga in OnePieceSaga, and searches for 
    a manually defined character book reference. (This is the boring part)
    The entire process will take a long time to execute. (More than a day)
    I had some memory issues and had to deal with those in a very "old fashioned" way (divide and conquer).
    """
    volumes = [f"{i:03d}" for i in range(1, 105)]
    for volume in volumes:
        print('-.'*25)
        print(f"\nProcessing volume: {volume}\n")
        print('-.'*25)
        
        gc.collect()
        os.makedirs(f"outputs/magiv2/v{volume}", exist_ok=True)
        os.makedirs(f"transcripts/v{volume}", exist_ok=True)
        chapter_pages = [f"data/v{volume}/{path}" for path in os.listdir(f"data/v{volume}")]

        saga = one_piece.get_saga_by_volume(int(volume))
        characters = os.listdir(f"character_images/{saga}")
        character_bank = {
            "images": [f"character_images/{saga}/{character}" for character in characters],
            "names": [character.replace(".png", "") for character in characters]
        }
        
        print("Converting character images to ndarrays...")
        chapter_pages = [read_image(x) for x in chapter_pages[110:]]
        character_bank["images"] = [read_image(x) for x in list(character_bank["images"])]

        print("Generating predictions for every page...")
        with torch.no_grad():
            per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)

        print(f"Writing transcript for volume: {volume}...")
        transcript = []
        for i, (image, page_result) in enumerate(zip(chapter_pages, per_page_results)):
            model.visualise_single_image_prediction(image, page_result, f"outputs/v{volume}/page_{i}.png")
            speaker_name = {
                text_idx: page_result["character_names"][char_idx] for text_idx, char_idx in page_result["text_character_associations"]
            }
            for j in range(len(page_result["ocr"])):
                if not page_result["is_essential_text"][j]:
                    continue
                name = speaker_name.get(j, "unsure") 
                transcript.append(f"<{name}>: {page_result['ocr'][j]}")


        with open(f"transcripts/v{volume}/transcript.txt", "w") as fh:
            for line in transcript:
                fh.write(line + "\n")
# Run script
if __name__ == "__main__":
    generate_transcripts() 