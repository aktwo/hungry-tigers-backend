from apscheduler.scheduler import Scheduler
import logging
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
  print '-'*50
  print 'Checking email now!'
  new_email = get_mail()
  if (current_email == None or current_email[0] != new_email[0]):
    current_email = new_email
    print 'New email!'
    print '\n'.join(new_email)
    print 'The parsed data is'
    sys.stdout.flush()
    print  process_input(' '.join(new_email[-2:]), buildings)
  else:
    print 'Sorry, nothing new here'
  sys.stdout.flush()

sched.start()

while True:
  pass
