import sqlite3
from flask import Flask, request, jsonify
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            status TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Save email log to SQLite
def save_email_log(email, status):
    conn = sqlite3.connect('emails.db')
    cursor = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO email_logs (email, status, timestamp)
        VALUES (?, ?, ?)
    ''', (email, status, timestamp))
    conn.commit()
    conn.close()

# Function to send emails
def send_email(sender_email, sender_password, recipient_emails, zip_path):
    subject = "🚀 Latest Executable File Attached – Please Review"
    body = """
    Dear Team,

    Please find attached the latest executable file for review.

    Best regards,
    Vivek
    """
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(recipient_emails)
    msg['Subject'] = subject

    body_part = MIMEText(body, 'plain')
    msg.attach(body_part)

    with open(zip_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(zip_path)}")
        msg.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_emails, msg.as_string())
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
    # Email credentials
    sender_email = 'uofaattacker@gmail.com'
    sender_password = ' bjqp sloj wuey myuj'  # App password for Gmail
    zip_path = 'execute.jpg'

    if not os.path.exists(zip_path):
        return jsonify({"error": f"Attachment file '{zip_path}' not found"}), 500

    result = send_email(sender_email, sender_password, recipient_emails, zip_path)

    # Log each email to the database
    for email in recipient_emails:
        status = "Success" if "status" in result else f"Error: {result['error']}"
        save_email_log(email, status)

    return jsonify(result)

if __name__ == "__main__":
    # Initialize the database when the app starts
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
