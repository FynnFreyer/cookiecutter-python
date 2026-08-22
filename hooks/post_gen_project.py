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
ORIGINAL_HOOK_FILE = Path(r"""{{ _cookiecutter_hook_file_path if _cookiecutter_hook_file_path is defined else (__file__ if not __file__.startswith(('/tmp/', '/var/tmp/')) else '') }}""")


def render_license(
    license_id: str,
    year: str,
    author: str,
    project_name: str,
    email: str,
) -> None:
    """Render a LICENSE file from the template repository's licenses/ directory.

    :param license_id: Identifier or name of the license (e.g. 'MIT', 'None').
    :param year: Copyright year.
    :param author: Author / copyright holder name.
    :param project_name: Name of the project.
    :param email: Author email address.
    :return: None
    """
    if license_id == "None":
        return

    template_file = None

    # 1. Check relative to original hook file if resolved
    if ORIGINAL_HOOK_FILE and ORIGINAL_HOOK_FILE.is_file():
        candidate = ORIGINAL_HOOK_FILE.resolve().parent.parent / "licenses" / f"{license_id}.txt"
        if candidate.exists():
            template_file = candidate

    # 2. Check relative to __file__ (in case hook was executed in place)
    if template_file is None:
        candidate = Path(__file__).resolve().parent.parent / "licenses" / f"{license_id}.txt"
        if candidate.exists():
            template_file = candidate

    # 3. Check current working directory and parents (in case cwd is in template or output dir)
    if template_file is None:
        candidate_dirs = [Path.cwd(), *Path.cwd().parents]
        for d in candidate_dirs:
            candidate = d / "licenses" / f"{license_id}.txt"
            if candidate.exists():
                template_file = candidate
                break

    if template_file is None:
        raise FileNotFoundError(f"License template for '{license_id}' not found.")

    text = template_file.read_text(encoding="utf-8")
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
    render_license(LICENSE_ID, YEAR, AUTHOR, PROJECT_NAME, EMAIL)
    init_git_repository(REPO_URL, REPO_ORG, PROJECT_NAME)
