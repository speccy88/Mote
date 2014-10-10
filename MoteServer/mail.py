# coding=utf8
import requests
import smtplib

class SendEmail:
    def __init__(self, msg="", subject="", sender='mote@server.net', to=['fred_blais5@hotmail.com']):
        self.sender = sender
        self.receivers = to
        self.subject = subject
        self.message = msg
        self.SetMSG()
        self.Connect()

    def SetMSG(self):
        self.email_content = "Subject: {}\n\n{}".format(self.subject,self.message)

    def Connect(self):
        pass
    
    def Disconnect(self):
        pass
        
    def Send(self):
        self.session.sendmail(self.sender,self.receivers,self.email_content)
        self.Disconnect()
        
class EmailGmail(SendEmail):
    def Connect(self):
        self.session = smtplib.SMTP('smtp.gmail.com:587')
        self.session.starttls()
        #self.session.login("email@email.com","password")
        
    def Disconnect(self):    
        self.session.quit()
        
class EmailVideotron(SendEmail):
    def Connect(self):
        self.session = smtplib.SMTP('relais.videotron.ca')

class EmailElectronicBox(SendEmail):
    def Connect(self):
        self.session = smtplib.SMTP('smtp.electronicbox.net:587')
 
def getISPcode():
    r = requests.get("http://ipinfo.io/json")
    ispInfo = r.json()["org"]
    ispCode = ispInfo[:6]
    return ispCode

def getSMTPserver():
    code = getISPcode()
    if code == "AS5769":
        return EmailVideotron()
    if code == "AS1403":
        return EmailElectronicBox()
    else:
        print code
        return EmailGmail()

if __name__=="__main__":     
    s = getSMTPserver()
    s.Send()
    
