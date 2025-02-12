import requests
import os
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# Google API KEY (Make sure to create one and save it in .env)
from dotenv import load_dotenv
load_dotenv()
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')

from saga_mapper_helper import OnePieceSaga
one_piece = OnePieceSaga()

# Output folder
OUTPUT_DIR = "character_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# This is not useful as most characters don't speak, and some have a design change.
def get_one_piece_characters() -> list:
    """Parse the webpage from OnePiece fandom to return a list of all characters."""

    url = "https://onepiece.fandom.com/wiki/List_of_Canon_Characters" 
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.tbody

    characters = []
    for row in table.find_all("tr")[1:]: # Remove header
        first_link = row.find("a") # get all anchor elements
        
        if first_link:
            character_name = first_link.get("title") #return only first cell
            characters.append(character_name)

    return set(characters)

def search_character_image(character:str, saga:str) -> str:
    """Use Google Custom Search API to find an image URL for a character."""
    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": character + "One Piece Character image" + saga.replace("_", " "),
        "cx": GOOGLE_CSE_ID,
        "key": GOOGLE_API_KEY,
        "searchType": "image",
        "num": 1,
    }
    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        results = response.json()
        if "items" in results:
            return results["items"][0]["link"]  # First image result
    return None


def download_and_save_image(character, image_url, saga) -> None:
    """From a given adress, attempt to download an image to a given character and save it."""
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))# Remove special case
            filename = f"{OUTPUT_DIR}/{saga}/{character.replace("/", "-")}.png"
            image.save(filename, format="PNG")
            print(f"✅ Saved: {filename}")
        else:
            print(f"❌ Failed to download: {image_url}")
    except Exception as e:
        print(f"❌ Error processing {character}: {e}")

def fetch_and_save_images():
    sagas = one_piece.character_mapper
    for saga, characters in sagas.items():
        os.makedirs(f"{OUTPUT_DIR}/{saga}", exist_ok=True)
        for character in characters:
            # Check if image already exists.
            if f"{character}.png" in os.listdir(f"{OUTPUT_DIR}/{saga}"):
                print(f"📑 {character} found in cache folder, skipping.")
                continue
            image_url = search_character_image(character, saga)
            if image_url:
                print(f"📸 Found image for {character}: {image_url}")
                download_and_save_image(character, image_url, saga)
            else:
                print(f"⚠️ No image found for {character}")
# Run script
if __name__ == "__main__":
    # fetch_and_save_images()
    print(search_character_image("Nami", "East Blue"))