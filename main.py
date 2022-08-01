from flask import Flask, render_template
app = Flask(__name__,static_folder='/')

from email import policy
from email.parser import BytesParser
import glob

@app.route('/')
def home():
    
    class Emails:
        Emails_DB = []
        def __init__(self, m_to, m_from, m_date, m_subj, m_id):
            self.m_to = m_to
            self.m_from = m_from
            self.m_date = m_date
            self.m_subj = m_subj
            self.m_id = m_id

        @classmethod
        def add_email_data(cls, m_to, m_from, m_date, m_subj, m_id):
            cls.Emails_DB.append(cls(m_to, m_from, m_date, m_subj, m_id))


    eml_dir = glob.glob(r'./sampleEmails/smallset/*.msg')
    
    s = '</td><td>'

    for eml_file in eml_dir:
        with open(eml_file, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)
            Emails.add_email_data(msg['to'], msg['from'], msg['date'], msg['subject'], msg['message-id'])
            #html += '<tr><td>' +  msg['to'] + s + msg['from'] + s + msg['date'] + s + msg['subject'] + s + msg['message-id'] + '</td></tr>'
    #for line in Emails.Emails_DB:
        #print('In line:', line, ' - ', line.m_from)

    return render_template('index.html', Emails_DB=Emails.Emails_DB)
if __name__ == "__main__":
  app.run(host ='0.0.0.0')