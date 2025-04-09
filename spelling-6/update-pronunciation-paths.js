const fs = require('fs');
const path = require('path');
const axios = require('axios'); // Make sure to install axios for fetching audio files

// Read the original pronunciations.json
const originalData = JSON.parse(fs.readFileSync('pronunciations.json', 'utf8'));

// Create the audio folder if it doesn't exist
const audioDir = path.join(__dirname, 'audio');
if (!fs.existsSync(audioDir)) {
    fs.mkdirSync(audioDir);
}

const updatedData = {};

async function downloadAudio(word, url) {
    const filePath = path.join(audioDir, `${word}.mp3`);

    // Check if the file already exists to avoid downloading multiple times
    if (!fs.existsSync(filePath)) {
        const writer = fs.createWriteStream(filePath);
        const response = await axios({ url, responseType: 'stream' });
        response.data.pipe(writer);
        return new Promise((resolve, reject) => {
            writer.on('finish', resolve);
            writer.on('error', reject);
        });
    }
    return Promise.resolve(); // Return a resolved promise if file already exists
}

async function updatePaths() {
    for (const word of Object.keys(originalData)) {
        const audioUrl = originalData[word];
        const filename = `${word}.mp3`;
        const filePath = path.join('audio', filename);

        try {
            // Download the audio file
            await downloadAudio(word, audioUrl);
            
            // Update the local path in the new format
            updatedData[word] = {
                word: word,
                audioFilePath: filePath
            };
        } catch (error) {
            console.error(`Error downloading audio for ${word}:`, error);
        }
    }

    // Save the updated paths to wordAudio.json in the audio directory
    fs.writeFileSync(path.join(audioDir, 'wordAudio.json'), JSON.stringify(updatedData, null, 2));
    console.log('✅ wordAudio.json updated with local audio paths.');
}

updatePaths().catch((err) => {
    console.error('Error in update process:', err);
});
