#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import codecs
import mail

"""
#récupérer la page pour le login
url_espace_client = 'https://www.videotron.com/client/residentiel/Espace-client'
r = requests.get(url_espace_client,verify=False)
ReqToFile(r)
"""
def ReqToFile(request):
    text = request.text
    text_file = codecs.open("out.html", "w", "ISO-8859-1")
    text_file.write(text)
    text_file.close()    
 
def SendSMSvideotron(msg, numero="418-376-2227"):
    url_login = 'https://www.videotron.com/client/user-management/residentiel/secur/Login.do'
    url_send_SMS = 'https://www.videotron.com/client/residentiel/secur/sansfil3G/sendSMS.do'
    post_data_login = {"dispatch":"login","appId":"EC","domain":"domainType.residential","cookieEnabled":"true","codeUtil":"speccy88","motDePasse":"f0xh0und"}    
    post_data_SMS = {"smsphone1":numero,"textesms":msg,"submit":"Send","smdsend":"true"}

    s = requests.Session()
    s.post(url_login, data=post_data_login, verify=False) #Il faut être identifié pour envoyer un sms
    s.post(url_send_SMS, data=post_data_SMS, verify=False)

def SendSMSbell(msg, numero="4185154491"):
    s = mail.getSMTPserver()
    s.message = msg
    s.receivers = numero+"@txt.bell.ca"
    s.Send()

def SendSMStelus(msg, numero="4183762227"):
    s = mail.getSMTPserver()
    s.message = msg
    s.SetMSG()
    s.receivers = [numero+"@msg.telus.com",]
    s.Send()

if __name__=="__main__":
    #SendSMSbell("Marie??")
    SendSMStelus("Je t'aime")
