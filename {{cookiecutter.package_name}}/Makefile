PACKAGE_NAME := {{cookiecutter.package_name}}
PACKAGE_DIR  := {{cookiecutter.module_name}}

CONDA_ENV_RUN   = conda run --no-capture-output --name $(PACKAGE_NAME)

TEST_ARGS := -v --cov=$(PACKAGE_NAME) --cov-report=term --cov-report=xml --junitxml=unit.xml --color=yes

.PHONY: env lint format test {% if cookiecutter.include_docs == "y" -%}docs-build docs-deploy{% endif %}

env:
	mamba create     --name $(PACKAGE_NAME)
	mamba env update --name $(PACKAGE_NAME) --file devtools/envs/base.yaml
	$(CONDA_ENV_RUN) pip install --no-deps -e .
	$(CONDA_ENV_RUN) pre-commit install || true

lint:
	$(CONDA_ENV_RUN) ruff check $(PACKAGE_DIR)

format:
	$(CONDA_ENV_RUN) ruff format $(PACKAGE_DIR)
	$(CONDA_ENV_RUN) ruff check --fix --select I $(PACKAGE_DIR)

test:
	$(CONDA_ENV_RUN) pytest -v $(TEST_ARGS) $(PACKAGE_DIR)/tests/

{% if cookiecutter.include_docs == "y" -%}
docs-build:
	$(CONDA_ENV_RUN) mkdocs build

docs-deploy:
ifndef VERSION
	$(error VERSION is not set)
endif
	$(CONDA_ENV_RUN) mike deploy --push --update-aliases $(VERSION)

{% if cookiecutter.include_griffe_insiders == "y" -%}
docs-insiders:
	$(CONDA_ENV_RUN) pip install git+https://$(INSIDER_DOCS_TOKEN)@github.com/{{cookiecutter.github_user}}/mkdocstrings-python.git \
                    			 git+https://$(INSIDER_DOCS_TOKEN)@github.com/{{cookiecutter.github_user}}/griffe-pydantic.git@fix-inheritence-static
{% endif %}
{% endif %}