import requests
from bs4 import BeautifulSoup
import json

# Words to fetch pronunciation for
words = ["ride", "bike", "perfect", "sleep", "healthy", "keep fit"]

def get_pronunciation(word):
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word.replace(' ', '-')}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent blocking
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        audio_div = soup.find("div", class_="sound audio_play_button pron-uk icon-audio")
        
        if audio_div:
            return audio_div["data-src-mp3"]
    
    return None  # Return None if no pronunciation found

# Scrape all words and store in dictionary
pronunciations = {word: get_pronunciation(word) for word in words}

# Save to JSON file
with open("pronunciations.json", "w") as json_file:
    json.dump(pronunciations, json_file, indent=4)

print("Pronunciations saved to pronunciations.json!")
