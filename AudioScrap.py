import requests
from bs4 import BeautifulSoup
import json

# Words to fetch pronunciation for
#words = ["ride", "bike", "perfect", "sleep", "healthy", "keep fit"]
words = ["sport", "learn", "unhealthy", "survey", "hours", "read"]

def get_pronunciation_and_ipa(word):
    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word.replace(' ', '-')}"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent blocking
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the audio URL based on the new structure
        audio_div = soup.find("div", class_="sound audio_play_button pron-uk icon-audio")
        audio_url = None
        if audio_div:
            audio_url = audio_div.get("data-src-mp3")
            if audio_url:
                audio_url = f"https://www.oxfordlearnersdictionaries.com{audio_url}"
        else:
            print(f"No audio found for {word}")

        # Scrape the IPA transcription based on the new structure
        ipa_tag = soup.find("span", class_="phon")
        ipa_text = None
        if ipa_tag:
            ipa_text = ipa_tag.text.strip()
        else:
            print(f"No IPA transcription found for {word}")

        return audio_url, ipa_text
    
    else:
        print(f"Failed to retrieve page for {word}, status code: {response.status_code}")
        return None, None

# Scrape all words and store both audio and IPA data in a dictionary
pronunciations = {}
for word in words:
    audio_url, ipa = get_pronunciation_and_ipa(word)
    if audio_url and ipa:
        pronunciations[word] = {"audio": audio_url, "ipa": ipa}
    else:
        print(f"Skipping {word}, missing audio or IPA.")

# Save to JSON file
with open("pronunciations.json", "w") as json_file:
    json.dump(pronunciations, json_file, indent=4)

print("Pronunciations saved to pronunciations.json!")
