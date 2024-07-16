import csv
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
import schedule
import time

# Load environment variables from .env file
load_dotenv()

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
CSV_FILE = 'recipients.csv'
CUSTOM_MESSAGE_FILE = 'message.txt'

# Function to read recipient emails from CSV file
def read_recipients_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        # Skip header row
        next(reader)
        recipients = [row[0] for row in reader]
    return recipients

# Function to read custom message from text file
def read_custom_message(file_path):
    with open(file_path, 'r') as file:
        message = file.read()
    return message

# Function to create email message with custom content
def create_email_message(custom_message):
    today = date.today().strftime("%Y-%m-%d")
    message = f"Daily Report - {today}\n\n"
    message += custom_message
    return message

# Function to send email
def send_email(recipients, custom_message):
    message = create_email_message(custom_message)

    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = ', '.join(recipients)
    msg['Subject'] = f"Daily Report - {date.today().strftime('%Y-%m-%d')}"

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to send daily report and manage duration
def send_daily_report():
    start_time = datetime.now()
    recipients = read_recipients_from_csv(CSV_FILE)
    custom_message = read_custom_message(CUSTOM_MESSAGE_FILE)
    
    # Send email to recipients
    send_email(recipients, custom_message)
    
    # Calculate duration
    duration = datetime.now() - start_time
    print(f"Script executed for {duration} seconds.")

# Schedule the job to run daily at a specific time (e.g., 12:00 PM)
schedule.every().day.at("12:25").do(send_daily_report)

# Run the script for 5 minutes
end_time = datetime.now() + timedelta(minutes=5)

# Run scheduled tasks until 5 minutes duration is completed
while datetime.now() < end_time:
    schedule.run_pending()
    time.sleep(1)

print("Script execution completed for 5 minutes.")
