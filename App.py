from flask import Flask, request, jsonify
import re
import socket

app = Flask(__name__)

@app.route('/validate-email', methods=['POST'])
def validate_email():
    data = request.get_json()
    email = data.get('email')

    # Perform email format validation using regular expressions
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
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


if __name__ == '__main__':
    app.run(debug=True)




## curl test.
## curl -X POST -H "Content-Type: application/json" -d "{\"email\":\"phil.wilkinson.premvan.com\"}" http://localhost:5000/validate-email