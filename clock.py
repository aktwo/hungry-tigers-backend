from apscheduler.scheduler import Scheduler
import time
import sys
from gmail_checker import get_mail

sched = Scheduler()

@sched.interval_schedule(seconds=5)
def timed_job():
  print '-'*50
  print 'Checking email now!'
  print '\n'.join(get_mail())
  sys.stdout.flush()

sched.start()

while True:
  pass
