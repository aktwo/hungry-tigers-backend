from apscheduler.scheduler import Scheduler
import logging
import requests
import json
import time
import sys
from gmail_checker import get_mail
from parser import *

logging.basicConfig()
sched = Scheduler()
buildings = get_buildings()
current_email = None

@sched.interval_schedule(seconds=30)
def timed_job():
  global current_email
  global buildings
  new_email = get_mail()
  if (current_email == None or current_email['uid'] != new_email['uid']):
    current_email = new_email
    print 'New email!'
    location_info = process_input(current_email['subject'] + ' ' + current_email['body'], buildings)
    params = {'listing': dict(current_email.items() + location_info.items())}
    headers = {'content-type': 'application/json'}
    requests.post('http://hungrytigers.herokuapp.com/new_listing', data = json.dumps(params), headers = headers)
    sys.stdout.flush()
  else:
    print 'Sorry, nothing new here'
  sys.stdout.flush()

sched.start()

while True:
  pass
