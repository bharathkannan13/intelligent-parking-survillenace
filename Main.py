from flask import Flask, render_template, flash, request, session
from flask import render_template, redirect, url_for, request
import mysql.connector
import datetime
import time
import easyocr
import sys

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/AdminLogin")
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb ")
    data = cur.fetchall()

    return render_template('AdminHome.html', data=data)


@app.route("/AdminReport")
def AdminReport():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrytb  ")
    data = cur.fetchall()
    return render_template('AdminReport.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':

        if request.form['Name'] == 'admin' and request.form['Password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')

            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()

            return render_template('AdminHome.html', data=data)

        else:
            data = "UserName or Password Incorrect!"

            return render_template('goback.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':

        name = request.form['t1']

        mobile = request.form['t2']
        email = request.form['t3']
        vno = request.form['t6']
        username = request.form['t4']
        Password = request.form['t5']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' or  VehicleNo='" + vno + "'")
        data = cursor.fetchone()
        if data:
            data = "Already Register  VehicleNo Or UserName!"
            return render_template('goback.html', data=data)

        else:
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into regtb values('','" + name + "','" + mobile + "','" + email + "','" + vno + "','" + username + "','" + Password + "','0')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
            cursor = conn.cursor()
            cursor.execute(
                "insert into multitb values('','" + vno + "','" + username + "','" + mobile + "','" + email + "')")
            conn.commit()
            conn.close()

            import LiveRecognition as liv

            liv.att()
            del sys.modules["LiveRecognition"]
            data = "Record Saved!"

            return render_template('goback.html', data=data)


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['Name']
        password = request.form['Password']
        # session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            alert = 'Username or Password is wrong'
            return render_template('goback.html', data=alert)



        else:
            session['vno'] = data[4]

            session['mo'] = data[2]
            session['em'] = data[3]

            session['uname'] = data[5]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():
    username = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  where username='" + username + "' ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route("/JoinUser")
def JoinUser():
    return render_template('JoinUser.html')


@app.route("/join", methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        uname = request.form['amt']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
        cursor = conn.cursor()
        cursor.execute(
            "insert into multitb values('','" + session['vno'] + "','" + uname + "','" + session['mo'] + "','" +
            session['em'] + "')")
        conn.commit()
        conn.close()

        import LiveRecognition as liv

        liv.att()
        del sys.modules["LiveRecognition"]
        data = "Record Saved!"

        return render_template('goback.html', data=data)


@app.route("/UserReport")
def UserReport():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrytb  where VehicleNo='" + session['vno'] + "' ")
    data = cur.fetchall()
    return render_template('UserReport.html', data=data)


@app.route("/Payment")
def Payment():
    # username = session['uname']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM amttb  where VehicleNo='" + session['vno'] + "' ")
    data = cur.fetchall()
    return render_template('Payment.html', data=data)


@app.route("/PaymentInfo")
def PaymentInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM amttb  ")
    data = cur.fetchall()
    return render_template('PaymentInfo.html', data=data)


@app.route("/Pay")
def Pay():
    session['id'] = request.args.get('id')
    session['amt'] = request.args.get('amt')
    return render_template('Pay.html', amt=session['amt'])


@app.route("/CardInfo")
def CardInfo():
    return render_template('CardInfo.html')


@app.route("/amount", methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        uname = session['uname']

        amt = request.form['amt']
        date = datetime.datetime.now().strftime('%Y-%b-%d')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
        cursor = conn.cursor()
        cursor.execute("SELECT  *  FROM   regtb where  UserName='" + uname + "'")
        data = cursor.fetchone()

        if data:

            price = data[7]

            Amount = float(price) + float(amt)

            print(Amount)


        else:
            return 'Incorrect username / password !'

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
        cursor = conn.cursor()
        cursor.execute("Update regtb set Amount='" + str(Amount) + "'  where  UserName='" + uname + "' ")
        conn.commit()
        conn.close()

        alert = 'Payment Successful'
        return render_template('goback.html', data=alert)


@app.route("/payy", methods=['GET', 'POST'])
def payy():
    if request.method == 'POST':
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
        cursor = conn.cursor()
        cursor.execute(
            "update amttb set Status='Paid' where id='" + session['id'] + "'  ")
        conn.commit()
        conn.close()

        alert = 'Payment Successful'
        return render_template('goback.html', data=alert)


def otp1():
    import random

    n = random.randint(1111, 9999)

    sendmsg(session['mob'], "Your OTP " + str(n))
    session['otp'] = n

    mmmsg = "Your OTP" + str(n);

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = session['email']

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = mmmsg

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    return render_template('In.html')


@app.route("/checkotp", methods=['GET', 'POST'])
def checkotp():
    if request.method == 'POST':
        vno = request.form['vno']

        if int(vno) == int(session['otp']):
            vno = session['vno']

            import datetime
            ts = time.time()
            date = datetime.datetime.now().strftime('%d-%b-%Y')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

            status = '0'

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
            cursor = conn.cursor()
            cursor.execute("SELECT * from regtb where VehicleNo='" + vno + "'")
            data = cursor.fetchone()
            if data is None:

                alert = 'VehicleNo Not Register '
                return render_template('goback.html', data=alert)

            else:

                for x in range(1, 200):
                    print(x)

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25vehicleparknumdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT * from entrytb where   Date='" + date + "' and Status='in'  and ParkingNo='" + str(
                            x) + "' ")
                    data = cursor.fetchone()
                    if data is None:
                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='25vehicleparknumdb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "insert into entrytb values('','" + vno + "','" + date + "','" + timeStamp + "','','in','" + str(
                                x) + "')")
                        conn.commit()
                        conn.close()
                        status = '1'

                        sendmsg(session['mob'], "Your Parking Slot Booked At:" + str(x))

                        return render_template('In.html', data=str(x))
                    else:
                        alert = 'Already Parking '
                        return render_template('goback.html', data=alert)

                if status == "0":
                    alert = 'Parking lot Full  '
                    return render_template('goback.html', data=alert)

        else:
            alert = 'OTP Incorrect..! '
            return render_template('goback.html', data=alert)


def otp2():
    import random

    n = random.randint(1111, 9999)

    sendmsg(session['mob'], "Your OTP " + str(n))
    session['otp'] = n

    mmmsg = "Your OTP" + str(n);

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = session['email']

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = mmmsg

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()

    return render_template('Out.html')


@app.route("/checkotp1", methods=['GET', 'POST'])
def checkotp1():
    if request.method == 'POST':
        vno = request.form['vno']

        if int(vno) == int(session['otp']):
            vno = session['vno']

            import datetime

            ts = time.time()
            date = datetime.datetime.now().strftime('%d-%b-%Y')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * from entrytb where vehicleno='" + vno + "' and Date='" + date + "' and Status='in'  ")
            data = cursor.fetchone()
            if data:
                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='25vehicleparknumdb')
                cursor = conn.cursor()
                cursor.execute(
                    "update entrytb set Status='out',OutTime='" + timeStamp + "' where vehicleno='" + vno + "' and Date='" + date + "' and Status='in'  ")
                conn.commit()
                conn.close()

                # start = datetime.datetime.strptime(str(data[3]), "%H:%M:%S")
                # end = datetime.datetime.strptime(str(data[4]), "%H:%M:%S")

                # difference =  start- end

                # seconds = difference.total_seconds()
                # print('difference in seconds is:', seconds)

                # minutes = seconds / 60
                # print('difference in minutes is:', minutes)

                amt = 100
                uname = session['uname']

                conn = mysql.connector.connect(user='root', password='', host='localhost',
                                               database='25vehicleparknumdb')
                cursor = conn.cursor()
                cursor.execute("SELECT  *  FROM   regtb where  UserName='" + uname + "'")
                data = cursor.fetchone()

                if data:

                    bal = data[7]

                    Amount = float(bal) - float(amt)

                    print(Amount)


                else:
                    return 'Incorrect username / password !'

                if Amount < 0:
                    alert = 'Amount Transaction Failed Balance:' + str(Amount)
                    return render_template('goback.html', data=alert)

                else:
                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25vehicleparknumdb')
                    cursor = conn.cursor()
                    cursor.execute(
                        "insert into amttb values('','" + uname + "','" + vno + "','" + date + "','" + str(
                            amt) + "','Paid')")
                    conn.commit()
                    conn.close()

                    sendmsg(session['mob'], "Your Parking Amount :" + str(amt), "thank you for visiting us")

                    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                   database='25vehicleparknumdb')
                    cursor = conn.cursor()
                    cursor.execute("Update regtb set Amount='" + str(Amount) + "'  where  UserName='" + uname + "' ")
                    conn.commit()
                    conn.close()

                    alert = ' vehicle out  '
                    return render_template('goback.html', data=alert)


            else:
                alert = ' vehicle is not parking  '
                return render_template('goback.html', data=alert)
        else:
            alert = 'OTP Incorrect..! '
            return render_template('goback.html', data=alert)


@app.route("/fin")
def fin():
    return In()


@app.route("/facelogin")
def facelogin():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb  ")
    data = cursor.fetchone()
    if data is None:

        alert = 'Face  Wrong '
        return render_template('goback.html', data=alert)


    else:
        session['vvno'] = data[2]

        return In()


@app.route("/fout")
def fout():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cursor = conn.cursor()
    cursor.execute(
        "truncate table temptb   ")
    conn.commit()
    conn.close()

    import LiveRecognition1 as liv1
    liv1.att()
    del sys.modules["LiveRecognition1"]
    return facelogin1()


@app.route("/facelogin1")
def facelogin1():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='25vehicleparknumdb')
    cursor = conn.cursor()
    cursor.execute("SELECT * from temptb  ")
    data = cursor.fetchone()
    if data is None:

        alert = 'Face  Wrong '
        return render_template('goback.html', data=alert)


    else:
        session['vvno'] = data[2]

        return Out()


@app.route("/In")
def In():
    session['vno'] = ''
    import cv2
    import re
    import torch
    from ultralytics import YOLO
    import easyocr
    import datetime
    import time

    # Load the YOLOv8 model
    model = YOLO('../runs/detect/anpr/weights/best.pt')

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # Add languages if needed

    # Open the video stream (0 for webcam, or provide video path)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Run YOLOv8 inference
        results = model(frame, conf=0.6)

        for result in results:
            if result.boxes:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
                    class_id = int(box.cls)
                    object_name = model.names[class_id]

                    # Extract the detected region
                    cropped_region = frame[y1:y2, x1:x2]

                    # Apply OCR on the cropped region
                    text_results = reader.readtext(cropped_region)
                    # print(text_results)

                    # Draw bounding box and detected text on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    if text_results:
                        detected_text = text_results[0][1]
                        cv2.putText(frame, detected_text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        print(f"Detected: {detected_text}")

                        vno = re.sub(r"[^a-zA-Z0-9]", "", detected_text)
                        print(vno)
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='25vehicleparknumdb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "select * from regtb where VehicleNo='" + str(vno) + "'  ")
                        data = cursor.fetchone()
                        if data is None:
                            print("VehilceNo Not Found")

                        else:
                            session['uname'] = data[5]
                            session['mob'] = data[2]
                            session['email'] = data[3]

                            session['vno'] = vno
                            cap.release()
                            cv2.destroyAllWindows()
                            return otp1()

        # Display the processed frame
        cv2.imshow("YOLOv8 + OCR", frame)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")


@app.route("/Out")
def Out():
    session['vno'] = ''
    import cv2
    import re
    import torch
    from ultralytics import YOLO
    import easyocr
    import datetime
    import time

    # Load the YOLOv8 model
    model = YOLO('../runs/detect/anpr/weights/best.pt')

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # Add languages if needed

    # Open the video stream (0 for webcam, or provide video path)
    cap = cv2.VideoCapture(0)

    flage = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Run YOLOv8 inference
        results = model(frame, conf=0.6)

        for result in results:
            if result.boxes:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Get bounding box coordinates
                    class_id = int(box.cls)
                    object_name = model.names[class_id]

                    # Extract the detected region
                    cropped_region = frame[y1:y2, x1:x2]

                    # Apply OCR on the cropped region
                    text_results = reader.readtext(cropped_region)
                    # print(text_results)

                    # Draw bounding box and detected text on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    if text_results:
                        detected_text = text_results[0][1]
                        cv2.putText(frame, detected_text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        print(f"Detected: {detected_text}")

                        vno = re.sub(r"[^a-zA-Z0-9]", "", detected_text)
                        print(vno)
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                       database='25vehicleparknumdb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "select * from temptb where VehicleNo='" + str(vno) + "'  ")
                        data = cursor.fetchone()
                        if data is None:
                            print("VehilceNo Not Found")

                        else:
                            session['uname'] = data[1]
                            session['mob'] = data[3]
                            session['email'] = data[4]

                            session['vno'] = data[2]
                            cap.release()
                            cv2.destroyAllWindows()
                            return otp2()

        cv2.imshow("YOLOv8 + OCR", frame)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


@app.route("/camera")
def camera():
    import cv2
    from ultralytics import YOLO

    dd1 = 0

    # Load the YOLOv8 model
    model = YOLO('yolo11n.pt')
    # Open the video file
    # video_path = "path/to/your/video/file.mp4"
    cap = cv2.VideoCapture(0)

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            # Run YOLOv8 inference on the frame
            results = model(frame, conf=0.6)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name == 'person':
                        dd1 += 1
                        print(dd1)
                    elif object_name == '':
                        dd1 = 0
                    else:
                        dd1 = 0

                    if dd1 == 50:
                        dd1 = 0

                        # import winsound

                        # filename = 'alert.wav'
                        # winsound.PlaySound(filename, winsound.SND_FILENAME)

                        annotated_frame = results[0].plot()

                        cv2.imwrite("alert.jpg", annotated_frame)
                        sendmail11()
                        # sendmsg(session['mob'], "Driver Action For:" + object_name)

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Inference", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()

    return render_template('index.html')


def sendmail11():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr = "kannanbharath015@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = "Drowsy Driver Detection"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    filename = "alert.jpg"
    attachment = open("alert.jpg", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "qmgn xecl bkqv musr")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
