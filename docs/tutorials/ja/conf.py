# Import src/conf.py
import os, sys
p = os.path.abspath('../../')
sys.path.insert(1, p)
from conf import *

language = 'ja'
root_doc = 'index'

templates_path = ['../../_templates']
html_static_path = ['../../_static']
html_logo = "../../_static/images/matlantis_white.png"
