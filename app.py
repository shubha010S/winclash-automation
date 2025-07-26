from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "✅ Winclash Automation API is Running!"})

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.get_json() or {}
    username = data.get("username", "")
    password = data.get("password", "")
    return jsonify({
        "status": "success",
        "username": username,
        "password": password,
        "message": "Account creation simulator"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
