# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath(os.pardir))


import nani


# -- General configuration ------------------------------------------------

needs_sphinx = '1.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'nani'
copyright = u"2016, Christopher Crouzet"
author = u"Christopher Crouzet"
version = nani.__version__
release = version
language = None

add_module_names = True
autodoc_member_order = 'bysource'
default_role = 'autolink'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
show_authors = False
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

if os.environ.get('READTHEDOCS', None) != 'True':
    try:
        import sphinx_rtd_theme
        html_theme = 'sphinx_rtd_theme'
        html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
    except ImportError:
        html_theme = 'alabaster'

html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = 'nanidoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
}

latex_documents = [
    (master_doc, 'nani.tex', u"nani Documentation",
     u"Christopher Crouzet", 'manual'),
]


# -- Options for manual page output ---------------------------------------

man_pages = [
    (master_doc, 'nani', u"nani Documentation",
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (master_doc, 'nani', u"nani Documentation", author, 'nani',
     "Alternative approach to defining and viewing NumPy's arrays.",
     'Miscellaneous'),
]
