import imaplib
import email
import time
import re

def get_mail():
  mail = imaplib.IMAP4_SSL('imap.gmail.com')
  mail.login('freefood.princeton@gmail.com', 'freefood333')

  mail.select("FreeFood") # connect to FreeFood folder
  result, data = mail.uid('search', None, "ALL")
  uids = data[0] # data is a list.
  uid_list = uids.split() # ids is a space separated string
  uid = uid_list[-1] # get the latest email's id

  result, data = mail.uid('fetch', uid, "(RFC822)")
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
  output = [time.asctime(date), sender, subject, body]
  return output
