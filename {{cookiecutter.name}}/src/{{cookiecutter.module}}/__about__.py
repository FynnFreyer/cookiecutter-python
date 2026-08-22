"""
This module contains meta-data for the {{cookiecutter.name}} project.
"""

# meta data
__project__ = "{{cookiecutter.name}}"
__description__ = "{{cookiecutter.description}}"
__version__ = "0.0.1.alpha"

# attribution
__org__ = ""
__authors__ = [
    {"name": "{{cookiecutter.full_name}}", "email": "{{cookiecutter.email}}"},
]
__maintainers__ = __authors__
__author_string__ = "; ".join(f"{author['name']} <{author['email']}>" for author in __authors__)
__copyright__ = f"Copyright (c) {{cookiecutter.year}} {__org__} {__author_string__}"
