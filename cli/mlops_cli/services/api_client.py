import requests
from mlops_cli.config import load_config, save_config

class APIClient:
    def __init__(self):
        cfg = load_config()
        self.base_url = cfg["server_url"]
        self.access_token = cfg.get("access_token")
        self.refresh_token = cfg.get("refresh_token")

    def _headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        resp = requests.request(method, url, headers=self._headers(), **kwargs)
        if resp.status_code == 401 and self.refresh_token:
            r = requests.post(f"{self.base_url}/auth/refresh",
                            json={"refresh_token": self.refresh_token})
            if r.status_code == 200:
                d = r.json()
                self.access_token = d["access_token"]
                self.refresh_token = d["refresh_token"]
                save_config(load_config() | d)
                resp = requests.request(method, url, headers=self._headers(), **kwargs)
        resp.raise_for_status()
        return resp.json()
