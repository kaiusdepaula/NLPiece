from transformers import AutoModel
import torch
import os

from utils import OnePieceSaga, read_image
one_piece = OnePieceSaga()

os.makedirs("outputs", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

model = AutoModel.from_pretrained("ragavsachdeva/magiv2", trust_remote_code=True).cuda().eval()

# volume = "002"
volumes = [f"{i:03d}" for i in range(2, 3)]
for volume in volumes:
    os.makedirs(f"outputs/v{volume}", exist_ok=True)
    os.makedirs(f"transcripts/v{volume}", exist_ok=True)
    chapter_pages = [f"data/v{volume}/{path}" for path in os.listdir(f"data/v{volume}")]

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
