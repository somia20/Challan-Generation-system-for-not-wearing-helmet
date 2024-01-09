from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from ultralytics import YOLO
from PIL import Image
import os
import io
from twilio.rest import Client
import base64
from flask_mail import Mail, Message
import sys

app = Flask(__name__)
app.secret_key = "Hello World"

## Database Connections
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Challan.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
with app.test_request_context():
     db.create_all()

# Load YOLO models
helmet_model = YOLO('C:\\Users\\HP\\Challan\\Generate-Challan\\helmet detection-challan generation\\models\\helmet_best.pt')
license_plate_model = YOLO('C:\\Users\\HP\\Challan\\Generate-Challan\\helmet detection-challan generation\\models\\best.pt')

# Define the upload folder and allowed extensions
UPLOAD_FOLDER = 'C:\\Users\\HP\\Challan\\Generate-Challan\\helmet detection-challan generation\\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Twilio credentials
account_sid = 'AC8d41ed2595d69e970142eb38ebe5f0a3'
auth_token = '44f4ccf360e54fe075f3bf67db04650d'
from_number = '+19252593534'
#to_number = '+91 7209578178'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "memcache"
app.config['SECRET_KEY'] = 'some random string'
### Configuration for Mails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'Asp82045@gmail.com'
app.config['MAIL_PASSWORD'] = 'isvyguwkoprmqywf'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
client = Client(account_sid, auth_token)

import random

# Predefined options for email and phone number
email_options = ['tanya.patel20@st.niituniversity.in', 'somia.kumari20@st.niituniversity.in', 'adya.tiwari20@st.niituniversity.in']
number_options = ['7209578178', '9876543210', '5551234567']

# Randomly select an email and phone number
random_email = random.choice(email_options)
random_number = random.choice(number_options)

def send_twilio_sms(message, to_number):
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

    return message.sid

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(input_path, output_folder, model, imgsz=320):
    results = model([input_path], imgsz=320)
    detected = False
    cropped_image_base64 = None  # Initialize the variable before the loop

    for i, result in enumerate(results):
        if len(result.boxes.xyxy) > 0:
            detected = True
            xyxy = result.boxes.xyxy[0]
            x_min, y_min, x_max, y_max = xyxy.tolist()

            # Crop the image using the bounding box coordinates
            cropped_image = Image.open(input_path).crop((x_min, y_min, x_max, y_max))

            # Save the cropped image
            output_path = os.path.join(output_folder, f'cropped_image_{i}.jpg')
            cropped_image.save(output_path)

            # Encode the cropped image to base64
            with io.BytesIO() as buffer:
                cropped_image.save(buffer, format="JPEG")
                cropped_image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return detected, cropped_image_base64

##### SQLlite Database
'''
Number Plate
Email id
Mobile Number
Date Time Created
'''
class Challan(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    numberPlate = db.Column(db.String(200), nullable=True)
    emailId = db.Column(db.String(200), nullable=True)
    mobileNumber = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.numberPlate}"


@app.route('/', methods=['GET', 'POST'])
def index():
    # For showing error if files not uploaded
    error_var='None'

    ### Variables which will be used by database
    if False:
        numberP = 'ch02af9157'
        email = ''
        num = ''
        challan = Challan(numberPlate=numberP, emailId=email, mobileNumber=num)
        db.session.add(challan)
        db.session.commit()

    allChallan = db.session.query(Challan).all()
    print(allChallan)



    if request.method == 'POST':
        
        # Check if the post request has the file part
        if 'file' not in request.files:
            error_var='No file part'

        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            error_var='No selected file'

        if file and allowed_file(file.filename):
            # Save the uploaded file
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(upload_path)

            # Process the uploaded image for helmet detection
            helmet_detected, helmet_img_base64 = process_image(upload_path, 'cropped_helmet_images', helmet_model)

            # Process the uploaded image for license plate detection
            license_plate_detected, license_plate_img_base64 = process_image(upload_path, 'cropped_license_plate_images', license_plate_model, imgsz=320)





            # Generate result message
            if helmet_detected and license_plate_detected:
                result_message = "No Challan Generated. Helmet Detected. Drive safely!"
                show_registered_info = False
            elif not helmet_detected and license_plate_detected:
                result_message = "Challan Generated for violating without helmet and with license plate!"
                numberP = "JK 04B 0946"
                email =  random_email
                num =  random_number
                challan = Challan(numberPlate=numberP, emailId=email, mobileNumber=num)
                db.session.add(challan)
                db.session.commit()
                show_registered_info = True
            else:
                result_message = "Challan Generated for violating without helmet and without license plate!"
                numberP = "JK 04B 0946"
                email =  random_email
                num =  random_number
                challan = Challan(numberPlate=numberP, emailId=email, mobileNumber=num)
                db.session.add(challan)
                db.session.commit()
                show_registered_info = True

            return render_template('Index_1.html', result=result_message, helmet_img=helmet_img_base64, license_plate_img=license_plate_img_base64, allChallan=allChallan,show_registered_info = show_registered_info)
    
    return render_template('Index_1.html', result=None, error=error_var, allChallan=allChallan)

# Route for updating the database
@app.route('/Update', methods=['GET', 'POST'])
def Updating_db():
    allChallan = db.session.query(Challan).all()
    return render_template('Updating_db.html', allChallan=allChallan)


### For deleting the Challan
@app.route('/delete/<int:sno>')
def delete(sno):
    report = Challan.query.filter_by(sno=sno).first()
    db.session.delete(report)
    db.session.commit()
    return redirect("/")


### Updating the the challan details
@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        numberPlate = request.form['numberPlate']
        emailId = request.form['emailId']
        mobileNumber = request.form['mobileNumber']
        year = request.form['year']
        month = request.form['month']
        date = request.form['date']
        
        Updatedreport = Challan.query.filter_by(sno=sno).first()
        
        Updatedreport.numberPlate = numberPlate
        Updatedreport.emailId = emailId
        Updatedreport.mobileNumber = mobileNumber
        Updatedreport.date_created = Updatedreport.date_created.replace(year=int(year), month=int(month), day=int(date))
        db.session.add(Updatedreport)
        db.session.commit()
        return redirect("/")
        
    challan = Challan.query.filter_by(sno=sno).first()
    return render_template('update.html', challan=challan)


### Updating the the challan details
@app.route('/SMS/<mnumber>', methods=['GET', 'POST'])
def smsSender(mnumber):
    send_twilio_sms("You have violated the traffic rule by not wearing the helmet for the vehicle license plate number - JK 04 B 0946, so therefore the challan is generated, and you have to pay the fine - Rs. 500.", to_number=mnumber)
    return redirect("/")

### API to send E-Mails
@app.route('/Email/<email>')
def emailSender(email):
    msg = Message("Challan Report", sender="noreply@demo.com", recipients=[email])
    body = "You have violated the traffic rule by not wearing the helmet for the vehicle license plate number - JK 04 B 0946, so therefore the challan is generated, and you have to pay the fine - Rs. 500."
    msg.body = body
    mail.send(msg)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
