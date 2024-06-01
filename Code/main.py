from ultralytics import YOLO
from collections import defaultdict
import datetime
import smtplib

class Media:
    def run(self):
        model = YOLO("yolov8n.pt")
        visited = defaultdict(list)

        stream = model.predict(source=hv.IP, show=True)
        #print(model.names) #all available objects to detect

        for frame in stream:
            boxes = frame.boxes
            for box in boxes:
                classIndex = int(box.cls[0])
                visited[model.names[classIndex]].append(datetime.datetime.now())
                
        email = Email()
        email.sendEmail(visited)
        
class Email:
    def sendEmail(self, data):
        #email configuration
        sender_email = hv.email
        receiver_email = hv.email
        password = hv.password  #password from 2 step authentication if gmail
        subject = "Data detected for today"
        
        string = ""
        
        for k, v in data.items():
            string += str(k) + " seen at " + str(v) + "\n\n"
        body = string

        message = f"""\
Subject: {subject}
From: {sender_email}
To: {receiver_email}

{body}
"""

        #connect to the SMTP server (in this case, Gmail's SMTP server)
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            #start TLS for security
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)

        print("Email sent successfully!")
        
class hiddenVariables:
    def __init__(self):
        self.password = "xxxx xxxx xxxx xxxx" #add email password, for gmail, it is in this format.
        self.IP = "http://admin:admin@000.000.0.000:0000" #add webcam IP
        self.email = "example@gmail.com" #add email to send object to
        
hv = hiddenVariables()
media = Media()
media.run()





