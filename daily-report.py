from datetime import datetime
import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
CSV_FILE = 'recipients.csv'
CUSTOM_MESSAGE_FILE = 'message.txt'

# Function to read recipient emails and names from CSV file
def read_recipients_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        recipients = [(row['email'], row['name']) for row in reader]
    return recipients

# Function to read custom message from text file
def read_custom_message(file_path):
    with open(file_path, 'r') as file:
        message = file.read()
    return message

# Function to create email message with custom content
def create_email_message(custom_message, recipient_name):
    today = datetime.today().strftime("%Y-%m-%d")
    message = f"Dear {recipient_name},\n\n"
    message += custom_message
    return message

# Function to send email
def send_email(recipient_email, recipient_name, custom_message):
    message = create_email_message(custom_message, recipient_name)

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = recipient_email
    msg['Subject'] = f"Report for - {datetime.today().strftime('%Y-%m-%d')}"

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"Email sent successfully to {recipient_name} ({recipient_email}).")
    except Exception as e:
        print(f"Failed to send email to {recipient_name} ({recipient_email}): {e}")

# Function to send daily report
def send_daily_report():
    start_time = datetime.now()
    recipients = read_recipients_from_csv(CSV_FILE)
    custom_message = read_custom_message(CUSTOM_MESSAGE_FILE)
    
    # Send email to each recipient
    for recipient_email, recipient_name in recipients:
        send_email(recipient_email, recipient_name, custom_message)
    
    # Calculate duration
    duration = datetime.now() - start_time
    print(f"Script executed for {duration} seconds.")

# Send the daily report once
send_daily_report()
print("Script execution completed.")
