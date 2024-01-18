import re

PACKAGE_REGEX = r"^[a-zA-Z][a-zA-Z0-9_-]+$"
MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"

package_name = "{{ cookiecutter.package_name }}"
module_name = "{{ cookiecutter.module_name }}"

if not re.match(MODULE_REGEX, module_name):
    print(f"ERROR: '{module_name}' is not a valid module name")
    exit(1)

if not re.match(PACKAGE_REGEX, package_name):
    print(f"ERROR: '{package_name}' is not a valid package name")
    exit(1)
