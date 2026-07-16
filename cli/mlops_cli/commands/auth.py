import click
import requests
from pathlib import Path
import json
from mlops_cli.config import save_config

@click.command()
@click.option("--server", required=True, help="Server URL (e.g. http://localhost:8000)")
def login(server):
    """Login to MLOps platform and save JWT token."""
    url = f"{server}/api/v1/auth/login"
    username = click.prompt("Username")
    password = click.prompt("Password", hide_input=True)

    resp = requests.post(url, json={"username": username, "password": password})
    if resp.status_code == 200:
        d = resp.json()
        cfg = {
            "server_url": f"{server}/api/v1",
            "access_token": d["access_token"],
            "refresh_token": d["refresh_token"],
        }
        save_config(cfg)
        click.echo("[OK] Login successful. Token saved.")
    else:
        click.echo(f"[FAIL] {resp.json().get('detail', 'Unknown error')}")
