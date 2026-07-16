import os
import tempfile
import zipfile

import click
import requests

from mlops_cli.services.api_client import APIClient


@click.command()
@click.argument("dataset_id")
@click.option("--version", "-v", type=int, default=None)
@click.option("--output", "-o", default=None)
def pull(dataset_id: str, version: int | None, output: str | None):
    """Download dataset to local directory."""
    api = APIClient()
    versions = api._request("GET", f"/datasets/{dataset_id}/versions")

    if version is not None:
        ver = [v for v in versions["items"] if v["version"] == version][0]
    else:
        ver = versions["items"][-1]

    dl = api._request("GET", f"/datasets/{dataset_id}/versions/{ver['id']}/download")
    out_dir = output or f"./dataset_{dataset_id}"
    os.makedirs(out_dir, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        archive = os.path.join(tmp, "dataset.zip")
        r = requests.get(dl["signed_url"], stream=True)
        r.raise_for_status()
        with open(archive, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        with zipfile.ZipFile(archive) as zf:
            zf.extractall(out_dir)

    click.echo(f"[OK] Dataset extracted to {out_dir}")
