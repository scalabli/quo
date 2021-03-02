from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

import quo.accordance

# compat until pallets-sphinx-themes is updated
quo.accordance.text_type = str

# Project --------------------------------------------------------------

project = "Quo
copyright = "2021 Secretum Inc"
author = "Gerrishon Sirere"
release, version = get_version("Quo", version_length=1)

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.log_cabinet",
    "pallets_sphinx_themes",
    "sphinx_issues",
    "sphinx_tabs.tabs",
]
intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
issues_github_path = "viewerdiscretion/quo"

# HTML -----------------------------------------------------------------

html_theme = "quo"
html_theme_options = {"index_sidebar_logo": False}
html_context = {
    "project_links": [
        ProjectLink("Donate", "https://buymeacoffee.com/secretum"),
        ProjectLink("PyPI Releases", "https://pypi.org/project/quo/"),
        ProjectLink("Source Code", "https://github.com/viewerdiscretion/quo/"),
        ProjectLink("Issue Tracker", "https://github.com/viewerdiscretion/quo/issues/"),
        ProjectLink("Website", "https:// quo.rtfd.io/"),
        ProjectLink("Twitter", "https://twitter.com/gerrishon_s"),
        
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_static_path = ["_static"]
html_favicon = "_static/quo.png"
html_logo = "_static/quo.png"
html_title = f"Quo Documentation ({version})"
html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [(master_doc, f"Click-{version}.tex", html_title, author, "manual")]
