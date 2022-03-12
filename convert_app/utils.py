import os
import zipfile

def zip_folder(dir_path: str, out_path_name: str) -> str:
    """Compress the specified folder into ZIP format

    Args:
        dir_path: Folder to be compressed
        out_path_name: Compressed file path
        For Example:
            dir_path: /home/user/image
            out_path_name: /home/user/image.zip
    """
    zip = zipfile.ZipFile(out_path_name, "w", zipfile.ZIP_DEFLATED)
    for _path, dirnames, filenames in os.walk(dir_path):
        fpath = _path.replace(dir_path, '')
        for filename in filenames:
            zip.write(os.path.join(_path, filename), os.path.join(fpath, filename))

