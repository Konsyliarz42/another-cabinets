import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

print("Searching for zip file")
zip_file = next(Path(".").glob("*.zip"))

print("Fething project: Farmer's Delight")
fd_project = requests.get("https://api.modrinth.com/v2/project/R2OftAxM")
fd_project.raise_for_status()
fd_project_data: dict = fd_project.json()

print("Fething last relase on GitHub")
release = requests.get(
    "https://api.github.com/repos/Konsyliarz42/another-cabinets/releases/latest",
    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ["GITHUB_TOKEN"]}",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
release.raise_for_status()
release_data: dict = release.json()

# https://docs.modrinth.com/#tag/versions/operation/createVersion
print("Preparing data for request")
headers = {
    "Authorization": os.environ["MODRINTH_TOKEN"],
    "User-Agent": f"https://github.com/Konsyliarz42/another-cabinets/tree/{release_data["name"]}",
    "Content-Type": "multipart/form-data",
}
data = {
    "name": release_data["name"],
    "version_number": release_data["name"],
    "changelog": release_data.get("body", None),
    "dependencies": [
        {  # Farmer's Delight
            "version_id": None,
            "project_id": "R2OftAxM",
            "file_name": None,
            "dependency_type": "optional",
        },
        {  # Farmer's Delight [Fabric]
            "version_id": None,
            "project_id": "4EakbH8e",
            "file_name": None,
            "dependency_type": "optional",
        },
        {  # Farmer's Delight Refabricated
            "version_id": None,
            "project_id": "7vxePowz",
            "file_name": None,
            "dependency_type": "optional",
        },
    ],
    "game_versions": fd_project_data["game_versions"],
    "version_type": "release",
    "loaders": ["minecraft"],
    "featured": False,
    "project_id": os.environ["MODRINTH_PROJECT_ID"],
    "file_parts": [zip_file.name],
}
files = {"file": zip_file.read_bytes()}

print("Sending a nev version")
response = requests.post(
    "https://api.modrinth.com/v2/version",
    headers=headers,
    data=data,
    files=files,
)
response.raise_for_status()
