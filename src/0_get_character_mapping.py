# import requests
from PIL import Image
import numpy as np
from transformers import AutoModel
from random import random, sample
import torch
import os

from utils import OnePieceSaga, read_image
one_piece = OnePieceSaga()

model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True).cuda().eval()

# Helper function to crop from pages random characters
def save_bbox(image: np.ndarray, bbox: list[float], saga: str) -> None:
    pil_image = Image.fromarray(image)
    x1, y1, x2, y2 = map(int, bbox)
    crop = Image.fromarray(image[y1:y2, x1:x2])
    filename = f"character_images/{saga}/{hash(random())}.png"
    try:
        crop.save(filename)
    except Exception as e:
        print(f"Failed with error: {e}")

# Output folder
OUTPUT_DIR = "character_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def sample_and_save_cropped_characters(sampled_pages:int) -> None:
    """Sample pages and volumes from whole sagas and save the identified rectangle on a folder for manual labelling evaluation."""
    if not sampled_pages:
        sampled_pages = 60

    for saga, volumes in one_piece.saga_mapper.items():
        os.makedirs(f"{OUTPUT_DIR}/{saga}", exist_ok=True)
        volume_lists = []  
        for volume in volumes:  
            volume_lists.extend([f"data/v{volume:03d}/{page}" for page in os.listdir(f"data/v{volume:03d}")])  
        sample_pages = sample(volume_lists, sampled_pages)

        chapter_pages = [read_image(x) for x in sample_pages]
        character_bank={"images":[], "names":[]}
        with torch.no_grad():
            per_page_results = model.do_chapter_wide_prediction(chapter_pages, character_bank, use_tqdm=True, do_ocr=True)

        for image, page_result in zip(chapter_pages, per_page_results):
            model.visualise_single_image_prediction(image, page_result)
            for bbox in page_result["characters"]:
                save_bbox(image, bbox, saga)



# Run script
if __name__ == "__main__":
    # Use code below with caution!
    sample_and_save_cropped_characters(sampled_pages=50) 