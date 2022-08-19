import json
import filedate
import sys
import os

from pathlib import Path


### USAGE:
### python modify_images.py PATH_TO_FOLDER_FROM_GOOGLE_EXPORT

### CONSTANTS:

FILE_EXCLUSIONS = ["print-subscriptions.json", "shared_album_comments.json", "user-generated-memory-titles.json", "metadata.json"]
METADATA_EXTENSIONS = [".json"]

### HELPER METHODS:

def find_match_media_files(source_dir, sought_file):
    # Most media, for whatever reason, doesn't use the complete image name
    # for the actual file name in the export
    # as such we use a hueristic of the following:
    # if meta file name length <= 35, use that name - .json for media filename
    # else use first 10 chars to find file
    results = []
    containing_text = sought_file.rstrip().lower().replace(".json", "")
    

    for i in range(1,30):
        if "(" + str(i) + ")" in containing_text:
            containing_text = containing_text.split(".")[0] + "(" + str(i) + ")"

    if len(sought_file.replace(".json", "")) > 35:
        containing_text = sought_file[0:35].lower()

    for root, dirs, files in os.walk(source_dir):
        for mediafilename in files:

            if containing_text in mediafilename.lower() and ".json" not in mediafilename.lower():
                results.append(mediafilename)

    if len(results) < 1:
        raise Exception("Found zero unique files for " + sought_file + " found " + str(results) + " used " + containing_text)
        #return None
    else:
        return results

### MAIN EXECUTION ########################################################################

print("Modify Images in place from " + sys.argv[1])

input_dir = sys.argv[1]

for root, dirs, files in os.walk(input_dir):
    for filename in files:
        if any((ext in filename.lower() and filename.lower() not in FILE_EXCLUSIONS) for ext in METADATA_EXTENSIONS):
            json_file_path = str(os.path.join(root, filename))

            metafile = open(json_file_path, "r")
            try:
                json_data = json.loads(metafile.read())
                metafile.close()
                media_file_paths = find_match_media_files(root, filename)

                # Note that we may get a single json file for both an image and video, etc.
                # if we do, simply update the timestamps for both
                for media_file_path in media_file_paths:
                    media_file = filedate.File(str(os.path.join(root, media_file_path)))
                    media_file.set(
                        created = json_data["photoTakenTime"]["formatted"],
                        modified = json_data["photoTakenTime"]["formatted"],
                        accessed = json_data["photoTakenTime"]["formatted"]
                    )
                json_file = filedate.File(str(os.path.join(root, json_file_path)))
                json_file.set(
                    created = json_data["photoTakenTime"]["formatted"],
                    modified = json_data["photoTakenTime"]["formatted"],
                    accessed = json_data["photoTakenTime"]["formatted"]
                )
            except:
                metafile.close()
                raise Exception("Unable to open file " + json_file_path)
