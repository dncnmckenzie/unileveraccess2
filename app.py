import os
import smtplib
from flask import Flask, render_template, request, redirect, url_for
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import base64

app = Flask(__name__)

# Environment variables for email credentials
EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL')

# Dummy data storage
visitors = []
vehicles = []
keys = []

def send_email(subject, body, to_email, signature_image=None):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # Use 'html' to support embedding images

    if signature_image:
        image_data = base64.b64decode(signature_image.split(',')[1])
        image = MIMEImage(image_data, name='signature.png')
        msg.attach(image)
        body += '<br><img src="cid:signature.png">'
        msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, to_email, text)
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/visitor_options')
def visitor_options():
    return render_template('visitor_options.html')

@app.route('/vehicle_options')
def vehicle_options():
    return render_template('vehicle_options.html')

@app.route('/key_options')
def key_options():
    return render_template('key_options.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_out')
def sign_out():
    return render_template('sign_out.html', visitors=visitors)

@app.route('/vehicle_sign_in')
def vehicle_sign_in():
    return render_template('vehicle_sign_in.html')

@app.route('/vehicle_sign_out')
def vehicle_sign_out():
    return render_template('vehicle_sign_out.html', vehicles=vehicles)

@app.route('/key_sign_in')
def key_sign_in():
    return render_template('key_sign_in.html')

@app.route('/key_sign_out')
def key_sign_out():
    return render_template('key_sign_out.html', keys=keys)

@app.route('/submit_sign_in', methods=['POST'])
def submit_sign_in():
    full_name = request.form['fullName']
    company = request.form['company']
    vehicle_registration = request.form['vehicleRegistration']
    mobile_number = request.form['mobileNumber']
    site_contact = request.form['siteContact']
    signature = request.form['signature']

    visitors.append({'full_name': full_name})

    subject = "Visitor Sign In Notification"
    body = f"""
    <p>Full Name: {full_name}</p>
    <p>Company: {company}</p>
    <p>Vehicle Registration: {vehicle_registration}</p>
    <p>Mobile Number: {mobile_number}</p>
    <p>Site Contact: {site_contact}</p>
    <p>Signature:</p>
    """

    send_email(subject, body, ADMIN_EMAIL, signature_image=signature)

    return redirect(url_for('dashboard'))

@app.route('/submit_sign_out', methods=['POST'])
def submit_sign_out():
    full_name = request.form['fullName']
    visitors[:] = [visitor for visitor in visitors if visitor['full_name'] != full_name]

    subject = "Visitor Sign Out Notification"
    body = f"<p>Visitor {full_name} has signed out.</p>"

    send_email(subject, body, ADMIN_EMAIL)

    return redirect(url_for('dashboard'))

@app.route('/submit_vehicle_sign_in', methods=['POST'])
def submit_vehicle_sign_in():
    full_name = request.form['fullName']
    company = request.form['company']
    vehicle_registration = request.form['vehicleRegistration']
    mobile_number = request.form['mobileNumber']
    site_contact = request.form['siteContact']
    signature = request.form['signature']

    vehicles.append({'full_name': full_name})

    subject = "Vehicle Sign In Notification"
    body = f"""
    <p>Full Name: {full_name}</p>
    <p>Company: {company}</p>
    <p>Vehicle Registration: {vehicle_registration}</p>
    <p>Mobile Number: {mobile_number}</p>
    <p>Site Contact: {site_contact}</p>
    <p>Signature:</p>
    """

    send_email(subject, body, ADMIN_EMAIL, signature_image=signature)

    return redirect(url_for('dashboard'))

@app.route('/submit_vehicle_sign_out', methods=['POST'])
def submit_vehicle_sign_out():
    full_name = request.form['fullName']
    vehicles[:] = [vehicle for vehicle in vehicles if vehicle['full_name'] != full_name]

    subject = "Vehicle Sign Out Notification"
    body = f"<p>Vehicle signed out by {full_name}.</p>"

    send_email(subject, body, ADMIN_EMAIL)

    return redirect(url_for('dashboard'))

@app.route('/submit_key_sign_in', methods=['POST'])
def submit_key_sign_in():
    full_name = request.form['fullName']
    key_number = request.form['keyNumber']
    company = request.form['company']
    mobile_number = request.form['mobileNumber']
    site_contact = request.form['siteContact']
    signature = request.form['signature']

    keys.append({'full_name': full_name})

    subject = "Key Sign In Notification"
    body = f"""
    <p>Full Name: {full_name}</p>
    <p>Company: {company}</p>
    <p>Key Number: {key_number}</p>
    <p>Mobile Number: {mobile_number}</p>
    <p>Site Contact: {site_contact}</p>
    <p>Signature:</p>
    """

    send_email(subject, body, ADMIN_EMAIL, signature_image=signature)

    return redirect(url_for('dashboard'))

@app.route('/submit_key_sign_out', methods=['POST'])
def submit_key_sign_out():
    full_name = request.form['fullName']
    keys[:] = [key for key in keys if key['full_name'] != full_name]

    subject = "Key Sign Out Notification"
    body = f"<p>Key signed out by {full_name}.</p>"

    send_email(subject, body, ADMIN_EMAIL)

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
