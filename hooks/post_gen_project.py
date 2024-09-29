import functools
import json
import os
import pathlib
import shutil
import subprocess
import urllib.error
import urllib.request

IS_PRIVATE = "{{ cookiecutter.private_repo }}" == "y"

REPO_NAME = "{{ cookiecutter.package_name }}"
REPO_ORG = "{{ cookiecutter.github_user }}"
REPO_URL = f"git@github.com:{REPO_ORG}/{REPO_NAME}.git"

REPO_DESCR = "{{ cookiecutter.description }}"

INCLUDE_DOCS = "{{ cookiecutter.include_docs }}" == "y"
INCLUDE_DATA = "{{ cookiecutter.include_data }}" == "y"
INCLUDE_CLI = "{{ cookiecutter.include_cli }}" == "y"
INCLUDE_INSIDERS = "{{ cookiecutter.include_griffe_insiders }}" == "y"

GH_TOKEN = os.environ.get("GITHUB_TOKEN")

if GH_TOKEN is None:
    raise RuntimeError("GITHUB_TOKEN environment variable not set.")

GH_PAGES_BRANCH = "gh-pages"
GH_PAGES_INDEX = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0;url=./latest/">
    <title>Redirecting to latest documentation</title>
</head>
<body>
    <p>If you are not redirected, <a href="./latest/">click here</a> to go to the latest documentation.</p>
</body>
</html>"""
GH_HEADERS = {
    "Authorization": f"token {GH_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json",
}
GH_USER = "{{ cookiecutter.github_user }}"


log = functools.partial(print, flush=True)


def invoke_shell(command: str, ignore_error: bool = True, print_output: bool = True):
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        output = e.output
        if not ignore_error:
            raise
    if print_output:
        log(output)
    return output


def initialize_git():
    """Initialize a git repository."""

    git_status = invoke_shell("git status", ignore_error=True, print_output=False)

    if "fatal" not in git_status:
        return

    log("Initializing git repository...")

    invoke_shell("git init --initial-branch=main")

    invoke_shell("git add .")
    invoke_shell("git commit -m 'Initial commit'")
    invoke_shell(f"git remote add origin {REPO_URL}")
    invoke_shell("git push -u origin main")


def initialize_gh_pages():
    """Initialize GitHub pages."""

    invoke_shell(f"git checkout --orphan {GH_PAGES_BRANCH}")
    invoke_shell("git rm -rf .")

    with open("index.html", "w") as file:
        file.write(GH_PAGES_INDEX)

    invoke_shell("git add index.html")
    invoke_shell("git commit -m 'Initial commit'")
    invoke_shell(f"git push origin {GH_PAGES_BRANCH}")
    invoke_shell(f"git checkout main")


def remove_docs():
    shutil.rmtree("docs")

    pathlib.Path("mkdocs.yml").unlink()
    pathlib.Path(".github/workflows/docs.yaml").unlink()


def remove_data():
    shutil.rmtree(pathlib.Path("{{cookiecutter.module_name}}/data"))


def remove_cli():
    pathlib.Path("{{cookiecutter.module_name}}/_cli.py").unlink()


def create_gh_repository():
    url = "https://api.github.com/user/repos"
    data = {"name": REPO_NAME, "description": REPO_DESCR, "private": IS_PRIVATE}

    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=GH_HEADERS, method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            response.read()
            log("Repository created successfully.")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Error creating repository: {e.read().decode()}") from e

    url = f"https://api.github.com/repos/{GH_USER}/{REPO_NAME}"
    data = {
        "has_projects": False,
        "has_wiki": False,
        "has_downloads": False,
        "allow_auto_merge": True,
        "allow_merge_commit": False,
        "allow_rebase_merge": False,
        "delete_branch_on_merge": True,
        "squash_merge_commit_titles": "PR_TITLE",
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=GH_HEADERS, method="PATCH"
    )
    try:
        with urllib.request.urlopen(req) as response:
            response.read()
            print("Repository settings updated successfully.")
    except urllib.error.HTTPError as e:
        print(f"Error updating repository settings: {e.read().decode()}")


def add_gh_pages_permissions():
    url = f"https://api.github.com/repos/{GH_USER}/{REPO_NAME}/actions/permissions/workflow"
    data = {
        "default_workflow_permissions": "write",
        "can_approve_pull_request_reviews": False,
    }
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=GH_HEADERS, method="PUT"
    )
    try:
        with urllib.request.urlopen(req) as response:
            response.read()
            log("Updated repository workflow permissions.")
    except urllib.error.HTTPError as e:
        raise RuntimeError(
            f"Error updating workflow permissions: {e.read().decode()}"
        ) from e


def enable_gh_pages():
    url = f"https://api.github.com/repos/{GH_USER}/{REPO_NAME}/pages"
    data = {"source": {"branch": "gh-pages", "path": "/"}}
    req = urllib.request.Request(
        url, data=json.dumps(data).encode("utf-8"), headers=GH_HEADERS, method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            response.read()
            log("Enabled GitHub Pages.")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Error enabling GitHub Pages: {e.read().decode()}") from e


if not INCLUDE_DOCS:
    log("Removing documentation...")
    remove_docs()
if not INCLUDE_DATA:
    log("Removing data...")
    remove_data()
if not INCLUDE_CLI:
    log("Removing CLI...")
    remove_cli()

create_gh_repository()
initialize_git()

if INCLUDE_DOCS:
    log("Initializing GitHub pages...")
    add_gh_pages_permissions()
    initialize_gh_pages()
    enable_gh_pages()

if INCLUDE_INSIDERS:
    log("You will need to manually create an action secret called `INSIDER_DOCS_TOKEN`")

if IS_PRIVATE:
    log("You will need to manually create an action secret called `CODECOV_TOKEN`")
