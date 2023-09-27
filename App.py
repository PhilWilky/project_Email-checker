from flask import Flask, request, jsonify, render_template
import re
import socket

app = Flask(__name__)

# Improved email regex pattern based on RFC 5322
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

@app.route('/validate-email', methods=['POST'])
def validate_email():
    data = request.get_json()
    email = data.get('email')

    # Check if 'email' is None or empty
    if email is None or email.strip() == '':
        return jsonify({'message': 'Email is missing'}), 400

    # Perform email format validation using the improved regular expression
    if not re.match(EMAIL_REGEX, email):
        return jsonify({'message': 'Invalid email format'}), 400

    # Split the email address to extract the domain
    _, domain = email.split('@')

    # Perform domain validation using DNS lookup
    try:
        # Get the domain's IP address (A record)
        ip_address = socket.gethostbyname(domain)
        if ip_address:
            return jsonify({'message': 'Domain is valid'}), 200
        else:
            return jsonify({'message': 'Domain does not exist'}), 400

    except socket.gaierror:
        return jsonify({'message': 'Invalid domain'}), 400

    # Implement checks for disposable email domains here

    # Return a success message if everything is valid
    return jsonify({'message': 'Email is valid'}), 200

# Create a Route for index.html:
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
