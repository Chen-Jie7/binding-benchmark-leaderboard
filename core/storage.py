from __future__ import annotations

import base64
import json

import requests
import streamlit as st

FILE_PATH = "data/submissions.json"


def _headers() -> dict:
    return {
        "Authorization": f"token {st.secrets['github_token']}",
        "Accept": "application/vnd.github.v3+json",
    }


def _api_url() -> str:
    repo = st.secrets["github_repo"]  # e.g. "Chen-Jie7/binding-benchmark-leaderboard"
    return f"https://api.github.com/repos/{repo}/contents/{FILE_PATH}"


def load_submissions() -> list[dict]:
    """Load submissions from the repo's submissions.json via GitHub API."""
    resp = requests.get(_api_url(), headers=_headers(), timeout=10)
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    content = base64.b64decode(resp.json()["content"]).decode()
    data = json.loads(content)
    return data.get("submissions", [])


def save_submission(entry: dict) -> None:
    """Append a submission and commit submissions.json back to the repo."""
    headers = _headers()

    # Get current file (need sha for update)
    resp = requests.get(_api_url(), headers=headers, timeout=10)
    if resp.status_code == 404:
        submissions = []
        sha = None
    else:
        resp.raise_for_status()
        file_data = resp.json()
        sha = file_data["sha"]
        content = base64.b64decode(file_data["content"]).decode()
        submissions = json.loads(content).get("submissions", [])

    submissions.append(entry)
    new_content = json.dumps({"submissions": submissions}, indent=2)
    encoded = base64.b64encode(new_content.encode()).decode()

    payload = {
        "message": f"Add submission: {entry.get('model_name', 'unknown')}",
        "content": encoded,
    }
    if sha:
        payload["sha"] = sha

    resp = requests.put(_api_url(), headers=headers, json=payload, timeout=10)
    resp.raise_for_status()
