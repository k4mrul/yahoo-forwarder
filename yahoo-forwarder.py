import smtplib, os
from imap_tools import MailBox

email = os.environ['email']  #email set to env
password = os.environ['password'] #password set to env
folder = 'forwardme'  #all emails from this folder will be forwarded. Create filter to put your preferred emails to this folder

fromMy = email
destination = os.environ['destinationEmail'] #destinationEmail set to env

mailbox = MailBox('imap.mail.yahoo.com')
mailbox.login(email, password)  

mailbox.folder.set(folder)
for msg in mailbox.fetch():
# for msg in mailbox.fetch(AND(seen=False)):
    stat = mailbox.folder.status(folder)

    #If email exist
    if stat.get('MESSAGES') > 0:

        message = 'Subject: {}\n\n{}'.format(msg.subject, msg.text)
        
        try:
            server = smtplib.SMTP("smtp.mail.yahoo.com",587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(email,password)
            server.sendmail(fromMy, destination, message)
            
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()    
        
        mailbox.move(mailbox.uids(), 'INBOX')  #move email to inbox after processing



