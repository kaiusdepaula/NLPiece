import requests
import os
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

# Output folder
OUTPUT_DIR = "character_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

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

# Function to search for an image of a character
def search_character_image(character:str) -> str:
    """Parse webpages from a specific character and get it's image adress."""
    # gallery-icon-container
    url = f"https://onepiece.fandom.com/wiki/{character.replace(" ", "_")}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup.find("a", class_="image image-thumbnail").get("href")


# Function to download and save images
def download_and_save_image(character, image_url) -> None:
    """From a given adress, attempt to download an image to a given character and save it."""
    
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))# Remove special case
            filename = f"{OUTPUT_DIR}/{character.replace("/", "-")}.png"
            image.save(filename, format="PNG")
            print(f"✅ Saved: {filename}")
        else:
            print(f"❌ Failed to download: {image_url}")
    except Exception as e:
        print(f"❌ Error processing {character}: {e}")

# Main function
def fetch_and_save_images():
    characters = get_one_piece_characters()

    for character in characters:
        # Check if image already exists.
        if f"{character}.png" in os.listdir(OUTPUT_DIR):
            print(f"📑 {character} found in cache folder, skipping.")
            continue
            
        image_url = search_character_image(character)
        if image_url:
            print(f"📸 Found image for {character}: {image_url}")
            download_and_save_image(character, image_url)
        else:
            print(f"⚠️ No image found for {character}")

# Run script
if __name__ == "__main__":
    fetch_and_save_images()