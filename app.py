from flask import Flask, jsonify

app = Flask(__name__)

#  Example of sensitive data (Bandit should detect this)
DB_PASSWORD = "SuperSecret123"

@app.route('/')
def home():
    return jsonify({"message": "Hello, Flask!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

