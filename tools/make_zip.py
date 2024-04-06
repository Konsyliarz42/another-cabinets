from argparse import ArgumentParser
from pathlib import Path
from zipfile import ZipFile

zip_content = [
    "assets",
    "pack.png",
    "pack.mcmeta",
]

parser = ArgumentParser()
parser.add_argument("-v", "--version", default="dev", type=str)
args = parser.parse_args()
zip_filename = f"another_cabinets-{args.version}.zip"

with ZipFile(Path(f"./{zip_filename}"), "w") as zip_file:
    for path_str in zip_content:
        path = Path(path_str)
        if path.is_dir():
            [zip_file.write(file) for file in path.glob("**/*")]
        else:
            zip_file.write(path)
