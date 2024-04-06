import os
from argparse import ArgumentParser
from pathlib import Path

import requests
from dotenv import load_dotenv

print("Searching for zip file")
zip_file = next(Path(".").glob("*.zip"))

print("Fething project: Farmer's Delight")
fd_project = requests.get("https://api.modrinth.com/v2/project/R2OftAxM")
fd_project.raise_for_status()

print("Parsing arguments")
parser = ArgumentParser()
parser.add_argument("--version", type=str, required=True)
parser.add_argument("--changelog", type=str, default="")

args = parser.parse_args()

print("Preparing data for request")
load_dotenv()

# https://docs.modrinth.com/#tag/versions/operation/createVersion
headers = {
    "Authorization": os.environ["MODRINTH_TOKEN"],
    "User-Agent": f"https://github.com/Konsyliarz42/another-cabinets/tree/{args.version}",
    "Content-Type": "multipart/form-data",
}
data = {
    "name": args.version,
    "version_number": args.version,
    "changelog": args.changelog or None,
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
    "game_versions": fd_project.json()["game_versions"],
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
