import smtplib
from email.mime.text import MIMEText

def send_email(receiver, message):

    # STEP 1: Replace with YOUR Gmail address
    sender_email = "gowslm2005@gmail.com"  # UPDATE THIS WITH YOUR GMAIL
    
    # STEP 2: Replace with YOUR Gmail App Password (16 characters, no spaces)
    # Get it from: https://myaccount.google.com/apppasswords
    # Example format: "abcdefghijklmnop" (remove spaces if copying)
    app_password = "aosjpxpsfitrytkz"

    msg = MIMEText(message)

    msg["Subject"] = "AI Agent Message"
    msg["From"] = sender_email
    msg["To"] = receiver

    try:
        print(f"Connecting to Gmail SMTP server...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        print(f"Logging in as: {sender_email}")
        server.login(sender_email, app_password)

        print(f"Sending email to: {receiver}")
        server.sendmail(sender_email, receiver, msg.as_string())

        server.quit()

        print("✓ Email sent successfully!")

    except Exception as e:
        print(f"❌ Email error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're using a Gmail App Password (not your regular password)")
        print("2. Enable 2-Factor Authentication: https://myaccount.google.com/security")
        print("3. Generate App Password: https://myaccount.google.com/apppasswords")
        print("4. Copy the 16-character password (remove spaces)")

