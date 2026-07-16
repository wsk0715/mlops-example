import os
import random
import tempfile
import zipfile
from uuid import UUID

import yaml

from app.services.storage_service import storage


def handle_upload(
    files: list,
    dataset_id: UUID,
    class_names: list[str],
    annotation_format: str,
) -> int:
    """
    Upload dataset zip -> extract -> validate -> split -> R2 -> data.yaml.

    Returns image_count.
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

            extract_dir = os.path.join(tmpdir, "extracted")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(extract_dir)

            images = _find_images(extract_dir)
            if not images:
                raise ValueError("No valid images found (.jpg/.jpeg/.png)")

            train, val = _split(images)

            version_prefix = f"datasets/{dataset_id}/v1/"
            _upload_to_r2(train, val, extract_dir, version_prefix)
            _create_data_yaml(extract_dir, class_names, version_prefix)

            return len(images)

    raise ValueError("No zip file found in upload")


def _find_images(extract_dir: str) -> list[str]:
    images = []
    valid = (".jpg", ".jpeg", ".png")
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.lower().endswith(valid):
                images.append(os.path.relpath(os.path.join(root, f), extract_dir))
    return images


def _split(images: list[str]):
    random.shuffle(images)
    split = int(len(images) * 0.8)
    return images[:split], images[split:]


def _upload_to_r2(train: list[str], val: list[str], base: str, prefix: str):
    for subset, split in (("train", train), ("val", val)):
        for rel in split:
            local = os.path.join(base, rel)
            r2_key = f"{prefix}images/{subset}/{os.path.basename(rel)}"
            storage.upload_file(local, r2_key)

            label_file = rel.rsplit(".", 1)[0] + ".txt"
            label_path = os.path.join(base, label_file)
            if os.path.exists(label_path):
                label_key = f"{prefix}labels/{subset}/{os.path.basename(label_file)}"
                storage.upload_file(label_path, label_key)


def _create_data_yaml(base: str, class_names: list[str], prefix: str):
    data = {
        "train": "./images/train",
        "val": "./images/val",
        "nc": len(class_names),
        "names": class_names,
    }
    import io

    yaml_bytes = yaml.dump(data, default_flow_style=False).encode()
    storage.upload_bytes(yaml_bytes, f"{prefix}data.yaml", content_type="text/yaml")
