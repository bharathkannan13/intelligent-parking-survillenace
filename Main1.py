import numpy as np
from tkinter import *
import os
from tkinter import filedialog
import cv2
import time, sys
from matplotlib import pyplot as plt
from tkinter import messagebox


def endprogram():
    print("\nProgram terminated!")
    sys.exit()


def testing():
    global testing_screen
    testing_screen = Toplevel(main_screen)
    testing_screen.title("Testing")
    # login_screen.geometry("400x300")
    testing_screen.geometry("600x450+650+150")
    testing_screen.minsize(120, 1)
    testing_screen.maxsize(1604, 881)
    testing_screen.resizable(1, 1)
    testing_screen.configure(bg='cyan')
    # login_screen.title("New Toplevel")

    Label(testing_screen, text='''Upload Image''', disabledforeground="#a3a3a3",
          foreground="#000000", width="300", height="2", bg='cyan', font=("Calibri", 16)).pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Label(testing_screen, text="").pack()
    Button(testing_screen, text='''Upload Image''', font=(
        'Verdana', 15), height="2", width="30", bg='cyan', command=imgtest).pack()


global affect


def imgtest():
    # import impre
    import_file_path = filedialog.askopenfilename()

    # image = cv2.imread(import_file_path)
    image = cv2.imread(import_file_path)
    from ultralytics import YOLO
    model = YOLO('runs/detect/anpr/weights/best.pt')

    # Run YOLOv8 inference on the image
    results = model(image, conf=0.1)

    # Annotate the image
    annotated_image = image.copy()

    for result in results:
        if result.boxes:
            for box in result.boxes:
                # Extract class ID and name
                class_id = int(box.cls)
                object_name = model.names[class_id]

                # Extract bounding box coordinates (x1, y1, x2, y2)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Calculate bounding box area
                width = x2 - x1
                height = y2 - y1
                area = width * height

                # Draw the bounding box and label
                cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{object_name}"
                cv2.putText(
                    annotated_image, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
                )

                print(f"Detected: {object_name}")

    # Display the annotated image
    cv2.imshow("YOLOv8 Prediction", annotated_image)
    cv2.waitKey(0)  # Wait for a key press to close the window
    cv2.destroyAllWindows()


def Camera1():
    import cv2
    import torch
    from ultralytics import YOLO
    import easyocr
    import re
    # Load the YOLOv8 model
    model = YOLO('runs/detect/anpr/weights/best.pt')

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

                    print(text_results)

                    # Draw bounding box and detected text on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    if text_results:
                        detected_text = text_results[0][1]

                        vno = re.sub(r"[^a-zA-Z0-9]", "", detected_text)
                        print(vno)

                        if vno == "TN37CR4019":
                            cap.release()
                            cv2.destroyAllWindows()

                        cv2.putText(frame, detected_text, (x1, y1 - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        print(f"Detected: {detected_text}")

        # Display the processed frame
        cv2.imshow("YOLOv8 + OCR", frame)

        # Break loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()



def Camera():
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
            results = model(frame, conf=0.4)
            for result in results:
                if result.boxes:
                    box = result.boxes[0]
                    class_id = int(box.cls)
                    object_name = model.names[class_id]
                    print(object_name)

                    if object_name == 'person':
                        dd1 += 1
                        print(dd1)
                    else:
                        dd1 = 0



                    if dd1 == 500:
                        dd1 = 0

                        #import winsound

                        #filename = 'alert.wav'
                        #winsound.PlaySound(filename, winsound.SND_FILENAME)

                        annotated_frame = results[0].plot()

                        cv2.imwrite("alert.jpg", annotated_frame)
                        sendmail()
                        #sendmsg(session['mob'], "Driver Action For:" + object_name)

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



def sendmail():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "projectmailm@gmail.com"
    toaddr ="kannanbharath015@gmail.com"

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



def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.configure()
    main_screen.title(" ANPR  Detection ")

    Label(text="  ANPR Detection", width="300", height="5", font=("Calibri", 16)).pack()

    Label(text="").pack()
    Button(text="Person", font=(
        'Verdana', 15), height="2", width="30", command=Camera).pack(side=TOP)
    Label(text="").pack()
    Button(text="Camera", font=(
        'Verdana', 15), height="2", width="30", command=Camera1).pack(side=TOP)

    main_screen.mainloop()


main_account_screen()
