"""
Hook that executes after the prompts ran and variables are defined.
"""

import subprocess


REPO_URL = "{{ cookiecutter.repo_url }}"
REPO_ORG = "{{ cookiecutter.repo_org }}"
PROJECT_NAME = "{{ cookiecutter.name }}"


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
    init_git_repository(REPO_URL, REPO_ORG, PROJECT_NAME)
