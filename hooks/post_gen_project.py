"""
Hook that executes after the prompts ran and variables are defined.
"""

import subprocess
from pathlib import Path

REPO_URL = "{{ cookiecutter.repo_url }}"
REPO_ORG = "{{ cookiecutter.repo_org }}"
PROJECT_NAME = "{{ cookiecutter.name }}"

LICENSE_ID = "{{ cookiecutter.license }}"
YEAR = "{{ cookiecutter.year }}"
AUTHOR = "{{ cookiecutter.full_name }}"
EMAIL = "{{ cookiecutter.email }}"
LICENSE_TEXT = """{{- cookiecutter._license_text -}}"""


def render_license(
    license_id: str,
    year: str,
    author: str,
    project_name: str,
    email: str,
    license_text: str = "",
) -> None:
    """Render a LICENSE file from the license text or local licenses directory.

    :param license_id: Identifier or name of the license (e.g. 'MIT', 'None').
    :param year: Copyright year.
    :param author: Author / copyright holder name.
    :param project_name: Name of the project.
    :param email: Author email address.
    :param license_text: Embedded license template text from Jinja context if available.
    :return: None
    """
    if license_id == "None":
        return

    text = license_text
    if not text:
        # Fallback to looking up license file from known relative paths
        template_paths = [
            Path(f"../licenses/{license_id}.txt"),
            Path(f"licenses/{license_id}.txt"),
            Path(__file__).resolve().parent.parent / "licenses" / f"{license_id}.txt",
        ]

        for candidate in template_paths:
            if candidate.exists() and candidate.is_file():
                text = candidate.read_text(encoding="utf-8")
                break

    if not text:
        raise FileNotFoundError(f"License template for '{license_id}' could not be loaded.")

    rendered = text.format(
        year=year,
        author=author,
        project_name=project_name,
        email=email,
        org="",
    )

    Path("LICENSE").write_text(rendered, encoding="utf-8")


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


if __name__ == "__main__":
    render_license(LICENSE_ID, YEAR, AUTHOR, PROJECT_NAME, EMAIL, LICENSE_TEXT)
    init_git_repository(REPO_URL, REPO_ORG, PROJECT_NAME)
