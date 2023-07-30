import requests

url = "https://api.elevenlabs.io/v1/models"

headers = {
  "Accept": "application/json",
  "xi-api-key": "1e92a485fb5c011d58945119747807fc"
}

response = requests.get(url, headers=headers)

print(response.text)