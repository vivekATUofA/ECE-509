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

## Disclaimer

This project is strictly for educational and research purposes. It was conducted in a controlled environment and does not endorse or support malicious activities. Always ensure compliance with ethical guidelines and cybersecurity best practices.

## License

This project is open-source under the [MIT License](LICENSE).

