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
REPO_DIR = r"{{ cookiecutter._repo_dir }}"
OUTPUT_DIR = r"{{ cookiecutter._output_dir }}"


def resolve_license_template(license_id: str) -> Path:
    template_file = None

    # Resolve REPO_DIR (if relative, resolve relative to OUTPUT_DIR or current directory)
    if REPO_DIR:
        repo_path = Path(REPO_DIR)
        if repo_path.is_absolute():
            candidate = repo_path / "licenses" / f"{license_id}.txt"
            if candidate.is_file():
                template_file = candidate
        else:
            # Check relative to OUTPUT_DIR (where cookiecutter was executed)
            if OUTPUT_DIR:
                candidate = (Path(OUTPUT_DIR) / repo_path / "licenses" / f"{license_id}.txt").resolve()
                if candidate.is_file():
                    template_file = candidate
            # Check relative to parent of generated project (cwd is generated project)
            if template_file is None:
                candidate = (Path.cwd().parent / repo_path / "licenses" / f"{license_id}.txt").resolve()
                if candidate.is_file():
                    template_file = candidate

    if template_file is None:
        raise FileNotFoundError(f"License template for '{license_id}' not found.")

    return template_file


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

    template_file = resolve_license_template(license_id)
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
