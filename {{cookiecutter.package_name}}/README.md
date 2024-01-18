<h1 align="center">{{cookiecutter.project_name}}</h1>

<p align="center">{{cookiecutter.description}}</p>

<p align="center">
  <a href="https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.package_name}}/actions?query=workflow%3Aci">
    <img alt="ci" src="https://github.com/{{cookiecutter.github_user}}/{{cookiecutter.package_name}}/actions/workflows/ci.yaml/badge.svg" />
  </a>
  <a href="https://codecov.io/gh/{{cookiecutter.github_user}}/{{cookiecutter.package_name}}/branch/main">
    <img alt="coverage" src="https://codecov.io/gh/{{cookiecutter.github_user}}/{{cookiecutter.package_name}}/branch/main/graph/badge.svg" />
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img alt="license" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
</p>

---

The `{{cookiecutter.package_name}}` framework ...

## Installation

This package can be installed using `conda` (or `mamba`, a faster version of `conda`):

```shell
mamba install -c conda-forge {{cookiecutter.package_name}}
```

{% if cookiecutter.include_docs == "y" -%}
## Getting Started

To get started, see the [documentation](https://{{ cookiecutter.github_user }}.github.io/{{ cookiecutter.package_name }}/latest/).
{% endif %}