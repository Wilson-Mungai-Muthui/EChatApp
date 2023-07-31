import pygame
import os
import aiohttp
import asyncio

CHUNK_SIZE = 1024
url = "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "1e92a485fb5c011d58945119747807fc"
}

currentLocation = (os.getcwd())


async def generateAudio(text, voice_id, language_id, file_path):
    global output_file
    data = {
        "text": text,
        "model_id":"eleven_multilingual_v1", 
        "voice_id": voice_id,
        "language_id": language_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    output_file = os.path.join(currentLocation, file_path)
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            with open(output_file, 'wb') as f:
                while True:
                    chunk = await response.content.read(CHUNK_SIZE)
                    if not chunk:
                        break
                    f.write(chunk)

    # Initialize pygame and play the .mp3 file
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()

    # Wait until the .mp3 file finishes playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


async def main():
    texts = [
        { "message": "Hi how are you doing today", "file_path": "output.mp3" },
        { "message": "I'm fine thank you", "file_path": "output2.mp3" },
        { "message": "Yeah, me too!", "file_path": "output3.mp3" },
    ]

    for text in texts:
        await generateAudio(text["message"], text["file_path"])

if __name__ == "_main_":
    asyncio.run(main())