# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys

sys.path.append('..')

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'QSimov Cloud Client'
copyright = '2023, QSimov Quantum Computing S.L.'
author = 'QSimov Quantum Computing S.L.'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

bibtex_bibfiles = ["references.bib"]

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.mathjax',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'nbsphinx',
    'sphinxcontrib.bibtex',
    'sphinx_copybutton'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/QSimov.svg"
html_css_files = ["custom.css"]

html_theme_options = {
    "collapse_navigation": True
}
html_context = {
  'display_github': True,
  'github_user': 'QSimovTech',
  'github_repo': 'qsimov-cloud-client',
  'github_version': 'main'
}
html_sidebars = {
    "**": ["search-field", "sidebar-nav-bs"]  # remove ads
}

