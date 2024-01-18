# Python Template

An opinionated template for Python projects that was originally based on the fantastic
[MolSSI Cookiecutter template](https://github.com/MolSSI/cookiecutter-cms), but has
now diverged significantly.

The template provides

- a basic python package project structure.
- a pre-commit configuration for linting and formatting using [`ruff`](https://github.com/astral-sh/ruff)
- a makefile with common commands, such as conda environment creation and linting.
- a GitHub Actions workflow for running tests and code coverage.
- automation to deploying documentation to GitHub Pages using GitHub Actions.
- simple GitHub issue / PR templates.

## Usage

To create a project using this template, run

```shell
cookiecutter gh:SimonBoothroyd/python-template
```

and follow the instructions.

### GitHub Pages

To enable automatic deployment of documentation to GitHub Pages, you will need to 
allow GitHub Actions to push to your repository. To do this, go to your repository's
settings page, and select `Actions -> General` from the left-hand menu. Then enable
`"Read and write permissions"` under `"Workflow permissions"`.

You will also need to enable GitHub Pages for your repository. To do this, go to your
repository's settings page, and select `Pages` from the left-hand menu. Then under 
`"Branch"`, select `gh-pages` and click `Save`.

You will probably also want to commit an `index.html` file to your repository `gh-pages`
branch that redirects to the latest documentation:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0;url=./latest/">
    <title>Redirecting to latest documentation</title>
</head>
<body>
    <p>If you are not redirected, <a href="./latest/">click here</a> to go to the latest documentation.</p>
</body>
</html>
```