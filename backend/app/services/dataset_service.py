import os
import tempfile
import zipfile

from app.services.storage_service import storage


def handle_upload(files: list, r2_key: str) -> int:
    """
    Upload dataset zip -> R2. Returns image_count.
    """
    if not files:
        raise ValueError("No files provided")

    for upload_file in files:
        if not upload_file.filename.endswith(".zip"):
            continue

        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "dataset.zip")
            content = upload_file.file.read()
            with open(zip_path, "wb") as f:
                f.write(content)

            image_count = _count_images_in_zip(zip_path)
            storage.upload_file(zip_path, r2_key)
            return image_count

    raise ValueError("No zip file found in upload")


def _count_images_in_zip(zip_path: str) -> int:
    valid = (".jpg", ".jpeg", ".png")
    count = 0
    with zipfile.ZipFile(zip_path, "r") as zf:
        for name in zf.namelist():
            if name.lower().endswith(valid):
                count += 1
    return count
