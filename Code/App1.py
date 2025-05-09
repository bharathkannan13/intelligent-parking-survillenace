from flask import Flask, render_template, flash, request, session

import mysql.connector
import sys

app = Flask(__name__)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/Home")
def Home():
    return render_template('index.html')


@app.route("/AdminLogin")
def DoctorLogin():
    return render_template('AdminLogin.html')




@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/NewProduct")
def NewProduct():
    return render_template('NewProduct.html')


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb  ")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/Report")
def Report():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrytb ")
    data = cur.fetchall()
    return render_template('Report.html', data=data)


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            flash("Login successfully")
            return render_template('AdminHome.html', data=data)

        else:
            flash("UserName Or Password Incorrect!")
            return render_template('AdminLogin.html')


@app.route("/Camera")
def Camera():
    import cv2
    import  re
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
                    #print(text_results)

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
                                                       database='3anprdb')
                        cursor = conn.cursor()
                        cursor.execute(
                            "select * from  regtb where vno='" + str(vno) + "'  ")
                        data = cursor.fetchone()
                        if data:
                            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                                           database='3anprdb')
                            cursor = conn.cursor()
                            cursor.execute(
                                "insert into entrytb values('','" + str(
                                    date) + "','" + str(
                                    timeStamp) + "','" + str(vno) + "')")
                            conn.commit()
                            conn.close()

                            cap.release()
                            cv2.destroyAllWindows()

        # Display the processed frame
        cv2.imshow("YOLOv8 + OCR", frame)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrytb ")
    data = cur.fetchall()
    return render_template('Report.html', data=data)





@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']
        vno = request.form['vno']
        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + address + "','"+ vno +"','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            session['vno'] = data[5]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM entrytb where Vno='" +  session['vno'] + "'")
            data = cur.fetchall()
            flash("Login successfully")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome():

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='3anprdb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM entrytb where Vno='" + session['vno'] + "'")
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
