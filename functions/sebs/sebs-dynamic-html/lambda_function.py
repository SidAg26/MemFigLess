from datetime import datetime                                                   
from random import sample  
from os import path
from time import time                                                           
import os

from jinja2 import Template

SCRIPT_DIR = path.abspath(path.join(path.dirname(os.path.abspath(__name__))))

def lambda_handler(event, context):

    # start timing
    name = "DYNAMIC-HTML_LAMBDA"
    size = event.get('n') if event.get('n') else 1000
    cur_time = datetime.now()
    random_numbers = sample(range(0, 1000000), size)
    template = Template( open(path.join(SCRIPT_DIR, 'templates', 'template.html'), 'r').read())
    html = template.render(username = name, cur_time = cur_time, random_numbers = random_numbers)
    # end timing
    # dump stats 
    return {'result': html}