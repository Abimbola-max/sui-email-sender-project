import os
import smtplib
from email.mime.text import MIMEText

from flask import Flask, jsonify, request

app = Flask(__name__)

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    if not data or 'email' not in data or 'message' not in data:
        return jsonify({"error": "Missing 'email' or 'message' field"}), 400

    recipient = data['email']
    message_body = data['message']

    msg = MIMEText(message_body)
    msg['Subject'] = "Message from Inheritance App"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = recipient

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, recipient, msg.as_string())
        return jsonify({"message": f"Email sent successfully to {recipient}"}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
