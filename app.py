from flask import Flask, request, redirect, render_template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Environment variables for email
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

print(f'EMAIL_USER: {EMAIL_USER}')
print(f'EMAIL_PASS: {EMAIL_PASS}')

def send_email(subject, body, to_email, signature_data=None):
    msg = MIMEMultipart('related')
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = subject

    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)

    html_body = f"""
    <html>
      <body>
        <p>{body.replace('\\n', '<br>')}</p>
    """
    if signature_data:
        html_body += f'<img src="{signature_data}">'

    html_body += """
      </body>
    </html>
    """

    msg_text = MIMEText(html_body, 'html')
    msg_alternative.attach(msg_text)

    try:
        with smtplib.SMTP('smtp.office365.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        print(f'Email sent to {to_email}')
    except Exception as e:
        print(f'Failed to send email: {e}')

@app.route('/')
def index():
    return render_template('index.html')

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
    return render_template('sign_out.html')

@app.route('/vehicle_sign_in')
def vehicle_sign_in():
    return render_template('vehicle_sign_in.html')

@app.route('/vehicle_sign_out')
def vehicle_sign_out():
    return render_template('vehicle_sign_out.html')

@app.route('/key_sign_in')
def key_sign_in():
    return render_template('key_sign_in.html')

@app.route('/key_sign_out')
def key_sign_out():
    return render_template('key_sign_out.html')

@app.route('/submit_sign_in', methods=['POST'])
def submit_sign_in():
    full_name = request.form['fullName']
    company = request.form['company']
    vehicle_registration = request.form['vehicleRegistration']
    mobile_number = request.form['mobileNumber']
    site_contact = request.form['siteContact']
    signature = request.form['signature']

    body = f"Visitor Sign In:\nName: {full_name}\nCompany: {company}\nVehicle: {vehicle_registration}\nMobile: {mobile_number}\nContact: {site_contact}"
    send_email("Visitor Sign In", body, "recipient@example.com", signature)
    return redirect('/')

@app.route('/submit_sign_out', methods=['POST'])
def submit_sign_out():
    full_name = request.form['fullName']
    body = f"Visitor Sign Out:\nName: {full_name}"
    send_email("Visitor Sign Out", body, "recipient@example.com")
    return redirect('/')

@app.route('/submit_key_sign_in', methods=['POST'])
def submit_key_sign_in():
    full_name = request.form['fullName']
    company = request.form['company']
    key_number = request.form['keyNumber']
    mobile_number = request.form['mobileNumber']
    site_contact = request.form['siteContact']
    signature = request.form['signature']

    body = f"Key Sign In:\nName: {full_name}\nCompany: {company}\nKey Number: {key_number}\nMobile: {mobile_number}\nContact: {site_contact}"
    send_email("Key Sign In", body, "recipient@example.com", signature)
    return redirect('/')

@app.route('/submit_key_sign_out', methods=['POST'])
def submit_key_sign_out():
    full_name = request.form['fullName']
    body = f"Key Sign Out:\nName: {full_name}"
    send_email("Key Sign Out", body, "recipient@example.com")
    return redirect('/')

@app.route('/submit_vehicle_sign_in', methods=['POST'])
def submit_vehicle_sign_in():
    full_name = request.form['fullName']
    company = request.form['company']
    vehicle_registration = request.form['vehicleRegistration']
    mobile_number = request.form['mobileNumber']
    site_contact = request.form['siteContact']
    signature = request.form['signature']

    body = f"Vehicle Sign In:\nName: {full_name}\nCompany: {company}\nVehicle: {vehicle_registration}\nMobile: {mobile_number}\nContact: {site_contact}"
    send_email("Vehicle Sign In", body, "recipient@example.com", signature)
    return redirect('/')

@app.route('/submit_vehicle_sign_out', methods=['POST'])
def submit_vehicle_sign_out():
    full_name = request.form['fullName']
    body = f"Vehicle Sign Out:\nName: {full_name}"
    send_email("Vehicle Sign Out", body, "recipient@example.com")
    return redirect('/')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
