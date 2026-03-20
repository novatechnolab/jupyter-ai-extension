import requests

API_KEY = "4B8hE9qHzx9NFdc5K6FLn16y"  # Get from https://dev.to/settings/account
url = "https://dev.to/api/articles"

article = {
    "article": {
        "title": "My Package Release v1.1.0",
        "body_markdown": "# My Package\n\nDescription here...",
        "published": True,
        "tags": ["python", "pypi", "package"]
    }
}

headers = {"api-key": API_KEY}
response = requests.post(url, json=article, headers=headers)
print(response.json())
