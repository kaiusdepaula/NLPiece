from PIL import Image
import numpy as np
from transformers import AutoModel
import torch
import os
import re

from saga_mapper_helper import OnePieceSaga
one_piece = OnePieceSaga()

os.makedirs("outputs", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True).cuda().eval()

def read_image(path_to_image):
    with open(path_to_image, "rb") as file:
        image = Image.open(file).convert("L").convert("RGB")
        image = np.array(image)
    return image

def extract_num(path):
    match = re.search(r'(\d+)(?=\D*$)', path)
    return int(match.group(1)) if match else float('inf')

volume = "001"
os.makedirs(f"outputs/v{volume}", exist_ok=True)
os.makedirs(f"transcripts/v{volume}", exist_ok=True)
chapter_pages = sorted([f"data/v{volume}/{path}" for path in os.listdir(f"data/v{volume}")], key=extract_num)

saga = one_piece.get_saga_by_volume(int(volume))
characters = one_piece.get_characters_by_volume(int(volume))

character_bank = {
    "images": [f"character_images/{saga}/{character}.png" for character in characters],
    "names": characters
}

chapter_pages = [read_image(x) for x in chapter_pages]
character_bank["images"] = [read_image(x) for x in list(character_bank["images"])]

with torch.no_grad():
    per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)

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
