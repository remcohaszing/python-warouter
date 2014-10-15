# -*- encoding: utf-8 -*-

import sys
import os

import pkg_resources

project = htmlhelp_basename = 'warouter'
pkg = pkg_resources.get_distribution(project)

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinxcontrib.napoleon'
]

intersphinx_mapping = {
    'python': ('http://docs.python.org/2.7', None),
    'webapp2': ('https://webapp-improved.appspot.com', None)
}

source_suffix = '.rst'
master_doc = 'index'
copyright = '2014, Remco Haszing'
release = version = pkg.version
pygments_style = 'sphinx'
html_theme = 'default'
