# app.py
import os
import json
import requests
import logging
from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.DEBUG)

load_dotenv()

app = Flask(__name__)

app.config.update({
    'MAIL_SERVER': 'smtp.gmail.com',
    'MAIL_PORT': 587,
    'MAIL_USE_TLS': True,
    'MAIL_USERNAME': os.getenv('MAIL_USERNAME'),
    'MAIL_PASSWORD': os.getenv('MAIL_PASSWORD'),
    'MAIL_DEFAULT_SENDER': os.getenv('MAIL_USERNAME'),
    'RECAPTCHA_SECRET_KEY': os.getenv('RECAPTCHA_SECRET_KEY'),
    'RECAPTCHA_SITE_KEY': os.getenv('RECAPTCHA_SITE_KEY')  # Add site key
})

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    try:
        with open('projects.json', 'r') as f:
            projects_data = json.load(f)
    except FileNotFoundError:
        logging.error("projects.json not found")
        projects_data = []
    return render_template('projects.html', projects=projects_data)

# app.py (partial update for contact route)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        recaptcha_secret = app.config['RECAPTCHA_SECRET_KEY']
        if not recaptcha_secret:
            logging.error("reCAPTCHA secret key missing")
            return jsonify({'status': 'error', 'message': 'Server configuration error: Missing reCAPTCHA secret key'}), 500

        try:
            recaptcha_verify = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                'secret': recaptcha_secret,
                'response': recaptcha_response
            }).json()
        except requests.RequestException as e:
            logging.error("reCAPTCHA verification request failed: %s", str(e))
            return jsonify({'status': 'error', 'message': 'Network error during reCAPTCHA verification'}), 500

        if not recaptcha_verify['success']:
            logging.warning("reCAPTCHA verification failed: %s", recaptcha_verify.get('error-codes', 'Unknown error'))
            return jsonify({'status': 'error', 'message': 'reCAPTCHA verification failed. Please try again.'}), 400

        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        if not all([name, email, message]):
            logging.warning("Form incomplete: name=%s, email=%s, message=%s", name, email, message)
            return jsonify({'status': 'error', 'message': 'All fields are required.'}), 400

        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=[os.getenv('MAIL_USERNAME')],
            body=f"Name: {name}\nregister:email: {email}\nMessage: {message}"
        )

        try:
            mail.send(msg)
            logging.info("Email sent successfully to %s", email)
            return jsonify({'status': 'success', 'message': 'Message sent successfully!'})
        except Exception as e:
            logging.error("Failed to send email: %s", str(e))
            return jsonify({'status': 'error', 'message': 'Failed to send message. Please try again later.'}), 500

    return render_template('contact.html', recaptcha_site_key=app.config['RECAPTCHA_SITE_KEY'])
if __name__ == '__main__':
    app.run(debug=True)