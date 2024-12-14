# Email Worm Attack Simulation

This project demonstrates the creation and propagation of an email worm within a controlled environment. It aims to highlight the potential risks and threats posed by email worms to individuals and organizations, showcasing how such worms can spread, collect sensitive information, and propagate further.

## Table of Contents
- [Introduction](#introduction)
- [Project Objectives](#project-objectives)
- [Technologies Used](#technologies-used)
- [Project Architecture](#project-architecture)
- [Experiments and Results](#experiments-and-results)
- [Challenges](#challenges)
- [Future Directions](#future-directions)

## Introduction

Email is a widely used communication tool, but it is also a common vector for cyberattacks. Email worms exploit this medium to spread malicious payloads, steal information, and disrupt systems. This project simulates an email worm attack to understand its mechanisms and potential impacts.

## Project Objectives

1. Analyze the mechanisms of email worm attacks.
2. Simulate an email worm attack in a controlled virtual environment.
3. Demonstrate how email worms propagate and collect sensitive data.
4. Provide insights into modern cybersecurity threats and their mitigation.

## Technologies Used

| **Category**         | **Technology**  | **Selection Criteria**                                                                 |
|-----------------------|-----------------|---------------------------------------------------------------------------------------|
| Infrastructure        | Virtual Machines | Collaboration and testing within the CLaaS environment.                              |
| Operating System      | Linux & Windows | Compatibility and ease of use for testing environments.                              |
| Programming Language  | Python          | Effective for implementing the email worm functionalities.                           |
| Email Providers       | Gmail           | Easy-to-use platform for sending and receiving emails.                               |
| Email Client          | Thunderbird     | Simplifies access to local email contacts.                                           |
| Protocols             | IMAP & POP3     | Enables downloading and accessing emails locally for programmatic interaction.       |

## Project Architecture

The email worm operates in the following stages:
1. **Reading Contacts and Information**: Extracts email contacts from the victim's email client or address book.
2. **Calling APIs**: Sends collected contact information to an attacker's server.
3. **Collecting Information**: Harvests data for spam, phishing campaigns, or database creation.
4. **Propagation**: Uses the collected contacts to send the worm to additional victims.

### Architecture Diagram
![Email Worm Attack Flow](images/EmailWormAttackFlow.png)

## Experiments and Results

### Key Experiments
1. **Email Contact Search**:
   - Extracts email contacts from Thunderbird installations on Windows and Linux systems.
   - Verified compatibility with different OS profiles and email configurations.

2. **Worm Propagation Simulation**:
   - Simulated worm behavior in a controlled environment.
   - Sent malicious payloads via email and measured propagation speed.

### Results
- Successfully extracted contact information from Thunderbird profiles.
- Simulated propagation in a virtualized environment, demonstrating the potential for rapid spread.
- Verified JSON formatting for collected data and API communication.

#### Example Output
![Test Result: Email Sent](images/Result_email_sent.png)

## Challenges

1. **Operating System Variability**:
   - Different OS configurations required flexible and adaptive path discovery methods.
   - Mitigated by implementing path searching for Thunderbird installations on both Windows and Linux.

2. **Modern Security Controls**:
   - Gmail's advanced security measures posed challenges for programmatic email access.
   - Used application-specific credentials and email clients to bypass restrictions.

## Future Directions

- Develop real-time detection systems for email worm behavior.
- Enhance collaboration for sharing threat intelligence among organizations.
- Explore AI-driven solutions for detecting polymorphic and zero-day worms.

# Email Sending Flask API with SQLite Logging

This project implements a Flask-based API for sending emails with attachments and logging the email transactions into an SQLite database. It provides an easy-to-use RESTful endpoint for bulk email sending.

## Features

- **REST API**: Exposes an endpoint to send emails via HTTP requests.
- **File Attachments**: Supports sending a ZIP file attachment.
- **Email Logging**: Logs each email transaction (success or failure) into an SQLite database.
- **Error Handling**: Captures and reports errors during email transmission.

## Requirements

- Python 3.7+
- Flask
- SQLite
- Required Python Libraries:
  - `flask`
  - `smtplib`
  - `sqlite3`
  - `email`
  - `os`

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

Install the required Python libraries using pip:

```bash
pip install flask
```

### 3. Prepare the Attachment

Place the file `gift_guide.zip` in the same directory as the script.

### 4. Configure Email Credentials

Update the `sender_email` and `sender_password` variables in the code:

- `sender_email`: Your Gmail address.
- `sender_password`: Gmail app password (not your regular password). [Learn more about app passwords](https://support.google.com/accounts/answer/185833?hl=en).

### 5. Run the Application

Start the Flask app by executing:

```bash
python <script_name>.py
```

The server will start and listen on `http://0.0.0.0:5000`.

### 6. Send Emails

Use a tool like `curl` or `Postman` to send a `POST` request to the `/send-email` endpoint.

#### Example Request:

```bash
curl -X POST http://localhost:5000/send-email \
-H "Content-Type: application/json" \
-d '{"emails": ["recipient1@example.com", "recipient2@example.com"]}'
```

#### Response:

```json
{
  "status": "Emails sent successfully"
}
```

### 7. Check Logs

The email transaction logs are stored in the SQLite database `emails.db`.

#### To View Logs:

Use a SQLite browser or run:

```bash
sqlite3 emails.db
SELECT * FROM email_logs;
```

## API Endpoint Details

### `POST /send-email`

**Request Body**:

- `emails` (required): A list of recipient email addresses.

Example:

```json
{
  "emails": ["recipient1@example.com", "recipient2@example.com"]
}
```

**Response**:

- Success: `{ "status": "Emails sent successfully" }`
- Failure: `{ "error": "<Error details>" }`

## Project Structure

```
project-directory/
│
├── emails.db           # SQLite database for email logs
├── gift_guide.zip      # Attachment file (ensure this exists)
├── <script_name>.py    # Main Flask application
├── README.md           # Project documentation (this file)
```

## Code Overview

### `init_db()`

- Initializes the SQLite database and creates the `email_logs` table if it does not exist.

### `save_email_log(email, status)`

- Saves each email transaction (status and timestamp) into the database.

### `send_email(sender_email, sender_password, recipient_emails, zip_path)`

- Sends emails with a specified ZIP file attachment.
- Handles errors during the email transmission process.

### `/send-email` API Endpoint

- Accepts a JSON request body containing recipient email addresses.
- Sends the emails and logs the transaction status.

## Security Notes

- Use a Gmail app password instead of your actual password for better security.
- Avoid hardcoding sensitive credentials in the code. Use environment variables or a configuration file.

## Disclaimer

This project is strictly for educational and research purposes. It was conducted in a controlled environment and does not endorse or support malicious activities. Always ensure compliance with ethical guidelines and cybersecurity best practices.

## License

This project is open-source under the [MIT License](LICENSE).

