import smtplib, ssl

EMAIL_ADDRESS = "LWOD@venturerei.com"
EMAIL_PASSWORD = "LWOD1234!"
# port = 465

# message = """\
#             Subject: Opendoor Event
            
#             This is Proactivated Appointment
#             xxx
#         """
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
#     server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, message)
    
    

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    
    subject = "Opendoor Event"
    body = "{0}\n{1}\n{2}".format("email", "pwd", "send")
    
    msg = f'Subject: {subject}\n\n{body}' 
    
    print(body)
    smtp.sendmail(EMAIL_ADDRESS, "katelove2716@gmail.com", msg)
    
    
