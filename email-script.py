import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Step 1: Read the file content
def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

# Step 2: Find all email addresses and put them into an array
def find_emails(content):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, content)
    return emails

# Step 3: Send the emails captured with subject "Sample Email"
def send_email(recipient, email_list):
    # Define sender's and recipient's email
    sender_email = "your.email@example.com"  # Replace with your email
    recipient_email = recipient
    
    # Set up the email content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Sample Email"
    
    # Create the email body
    body = "Found emails:\n" + "\n".join(email_list)
    message.attach(MIMEText(body, "plain"))

    # Send the email (requires a configured SMTP server)
    try:
        with smtplib.SMTP("smtp.example.com", 587) as server:  # Replace with your SMTP server
            server.starttls()
            server.login(sender_email, "your_password")  # Replace with your email and password
            server.sendmail(sender_email, recipient_email, message.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print("Error sending email: {e}")

# Example usage
file_path = "INBOX.msf"  # Replace with the path to your file
content = read_file(file_path)
emails = find_emails(content)

# Output emails found for verification
print("Emails found:", emails)

# Send the found emails to the recipient
send_email("recipient.email@example.com", emails)  # Replace with actual recipient
