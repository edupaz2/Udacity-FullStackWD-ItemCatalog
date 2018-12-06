#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)

sys.path.insert(0,"/home/ubuntu/catalog")
from myapp import app as application

application.secret_key = 'catalog secret key'
