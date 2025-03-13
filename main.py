import argparse
import asyncio
import logging
import os
import shutil
from pathlib import Path

# Setting up error logging
logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)

from pathlib import Path

# Define the source folder
source_folder = Path("source_files")
source_folder.mkdir(exist_ok=True)

# Define sample files with content
files_content = {
    "note.txt": "Hello, this is a sample text file.",
    "data.csv": "id,name,age\n1,John,30\n2,Jane,25",
    "report.pdf": "This is a dummy PDF file.",
    "image.png": "",
    "script.py": "print('Hello, world!')",
    "README": "This file has no extension.",
    "presentation.pptx": "This is a dummy PowerPoint file.",
    "archive.zip": "This is a dummy ZIP file.",
    "music.mp3": "This is a dummy MP3 file.",
    "video.mp4": "This is a dummy MP4 file.",
    "document.docx": "This is a dummy Word document.",
}

for filename, content in files_content.items():
    file_path = source_folder / filename
    file_path.write_text(content)

 # Asynchronously copies a file into a subfolder of the destination directory based on its extension.
async def copy_file(file_path: Path, output_folder: Path):
   
    try:
        # Get the file extension (without the dot) or 'no_extension' for files without an extension
        ext = file_path.suffix[1:] if file_path.suffix else "no_extension"
        dest_folder = output_folder / ext
        # Create the destination subfolder if it does not exist
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_file = dest_folder / file_path.name
        # Perform file copy asynchronously
        await asyncio.to_thread(shutil.copy2, file_path, dest_file)
    except Exception as e:
        logging.error(f"Error copying file {file_path}: {e}")

#  Asynchronously reads all files from the source folder (recursively) and copies them.
async def read_folder(source_folder: Path, output_folder: Path):
    
    try:
        # Perform recursive retrieval of the list of files in a separate thread
        files = await asyncio.to_thread(
            lambda: [
                Path(root) / file
                for root, _, files in os.walk(source_folder)
                for file in files
            ]
        )
        tasks = [
            asyncio.create_task(copy_file(file_path, output_folder))
            for file_path in files
        ]
        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        logging.error(f"Error reading folder {source_folder}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Asynchronous file sorting by extension"
    )
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("output_folder", help="Path to the destination folder")
    args = parser.parse_args()

    source_folder = Path(args.source_folder)
    output_folder = Path(args.output_folder)

    # Check if the source folder exists
    if not source_folder.exists() or not source_folder.is_dir():
        logging.error("The source folder does not exist or is not a directory.")
        return

    # Create the destination folder if it does not exist
    output_folder.mkdir(parents=True, exist_ok=True)

    # Start the asynchronous file sorting process
    asyncio.run(read_folder(source_folder, output_folder))


if __name__ == "__main__":
    main()
