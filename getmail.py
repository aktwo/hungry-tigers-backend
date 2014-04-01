import imaplib
import email
import time
import re

def getUID(mail):
  mail.select("FreeFood") # connect to FreeFood folder

  result, data = mail.uid('search', None, "ALL")
  uids = data[0] # data is a list.
  uid_list = uids.split() # ids is a space separated string
  return uid_list[-1] # get the latest email's id
 



mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('freefood.princeton@gmail.com', 'freefood333')

saved_uid = -1
while True:
  # check every 5 seconds
  latest_uid = getUID(mail)
  if latest_uid == saved_uid:
    print latest_uid
    time.sleep(5)
    continue
  saved_uid = latest_uid

  result, data = mail.uid('fetch', latest_uid, "(RFC822)")
  raw_email = data[0][1] # here's the body, which is raw text of the whole email
  # including headers and alternate payloads

  email_message = email.message_from_string(raw_email)

  sender = email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>
  date = email.utils.parsedate(email_message['Date'])

  # clean up subject text
  subject_raw = email_message['Subject']
  subject_re = re.compile('\[FreeFood\]\s+')
  split = subject_re.split(subject_raw)
  subject = split[-1]

  body_raw = ''
  for part in email_message.walk():
    # each part is a either non-multipart, or another multipart message
    # that contains further parts... Message is organized like a tree
    if part.get_content_type() == 'text/plain':
        body_raw = part.get_payload() # prints the raw text

  body_re = re.compile('\s*-----\s+You are receiving')
  split = body_re.split(body_raw)
  body = split[0]

  print time.asctime(date)
  print subject
  print body

  #print email_message.items() # print all headers

