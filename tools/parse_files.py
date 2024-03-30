import os

def parse_filenames(dir_name: str, ext: str):
    filenames = []
    for root, dirs, files in os.walk(dir_name):
        if len(files) > 0:
            # Append only files with the specified extension
            filenames.extend([os.path.join(root, f) for f in files if f.endswith(ext)])
    return filenames
