# Google Photos Fixer
As it stands today (Aug 2022), pictures downloaded/exported from google photos come with the wrong creation date. This tool iterates an export of google photoes (taken from Google Takeouts), and modifies all media files to have a created/modified/accessed date of the media-taken timestamp from the exif metadata, etc.

## Install deps:
pip install -r requirements.txt

## Usage

**NOTE**: This process modifies in place. If that's not your cup of tea, feel free to run the tool against a copy of your raw export data.

To use, simply:

```
    python modify_images.py FULL_PATH_TO_EXTRACTED_EXPORT
```