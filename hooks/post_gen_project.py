import os
import pathlib
import shutil
import subprocess


def invoke_shell(command, expected_error=True, print_output=True):
    try:
        output = subprocess.check_output(
            command, shell=True, stderr=subprocess.STDOUT, text=True
        )
    except subprocess.CalledProcessError as e:
        print(e.output)
        output = e.output
        if not expected_error:
            raise e
    if print_output:
        print(output)
    return output


def initialize_git():
    """Initialize a git repository."""

    git_status = invoke_shell("git status", expected_error=True, print_output=False)

    if 'fatal' not in git_status:
        return

    print("initializing git repository...")

    invoke_shell("git init --initial-branch=main")

    invoke_shell("git add .")
    invoke_shell("git commit -m \"Initial commit.\"")


def remove_docs():
    include_docs = '{{ cookiecutter.include_docs }}'

    if include_docs == "y":
        return

    shutil.rmtree("docs")

    pathlib.Path("mkdocs.yml").unlink()
    pathlib.Path(".github/workflows/docs.yaml").unlink()


def remove_data():
    include_data = '{{ cookiecutter.include_data }}'

    if include_data == "y":
        return

    shutil.rmtree(pathlib.Path("{{cookiecutter.module_name}}/data"))


def remove_cli():
    include_cli = '{{ cookiecutter.include_cli }}'

    if include_cli == "y":
        return

    pathlib.Path("{{cookiecutter.module_name}}/_cli.py").unlink()


remove_docs()
remove_data()
remove_cli()

initialize_git()
