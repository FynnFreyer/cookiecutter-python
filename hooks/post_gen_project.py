"""
Hook that executes after the prompts ran and variables are defined.
"""

import json
import re
import subprocess
from pathlib import Path
from urllib.request import urlopen

REPO_URL = "{{ cookiecutter.repo_url }}"
REPO_ORG = "{{ cookiecutter.repo_org }}"
PROJECT_NAME = "{{ cookiecutter.name }}"


LICENSE_ID = "{{ cookiecutter.license }}"
YEAR = "{{ cookiecutter.year }}"
AUTHOR = "{{ cookiecutter.full_name }}"


def init_git_repository(repo_url: str, repo_org: str, project_name: str) -> None:
    """Initialize a git repository and perform the initial commit and push.

    :param repo_url: Host URL or domain for the repository (e.g., 'github.com').
    :param repo_org: Git organization or user namespace.
    :param project_name: Project repository name.
    :return: None
    :raises subprocess.CalledProcessError: If any underlying git command fails.
    """
    remote_target = f"git@{repo_url}:{repo_org}/{project_name}"
    commit_msg = f"init: init {project_name} project from cookiecutter-python template"

    commands = [
        ["git", "init"],
        ["git", "remote", "add", "origin", remote_target],
        ["git", "add", "."],
        ["git", "commit", "-m", commit_msg],
        ["git", "push", "--set-upstream", "origin", "main"],
    ]

    # Ensure execution halts immediately if a git pipeline step fails
    for cmd in commands:
        subprocess.run(cmd, check=True)


def generate_license_file(spdx_id: str, year: str, author: str) -> None:
    """
    Fetch and render an SPDX license to a local LICENSE file.

    :param spdx_id: SPDX short identifier (e.g., 'MIT', 'Apache-2.0').
    :param year: Copyright year.
    :param author: Copyright holder name.
    :return: None
    :raises Exception: If the license cannot be retrieved or written.
    """
    # Fetch license details from the official SPDX JSON dataset
    url = f"https://raw.githubusercontent.com/spdx/license-list-data/main/json/details/{spdx_id}.json"
    with urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))

    template = data.get("standardLicenseTemplate", data.get("licenseText", ""))

    # Clean SPDX variable tags and inject user metadata
    text = re.sub(
        r'<<var;name="copyright";original=(.*?);match=.*?>>',
        f"Copyright (c) {year} {author}",
        template,
        flags=re.DOTALL,
    )
    text = re.sub(r"<<beginOptional>>|<<endOptional>>", "", text)

    Path("LICENSE").write_text(text)


if __name__ == "__main__":
    init_git_repository(REPO_URL, REPO_ORG, PROJECT_NAME)
    if LICENSE_ID != "None":
        generate_license_file(LICENSE_ID, YEAR, AUTHOR)
