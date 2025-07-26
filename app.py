from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "✅ Winclash Automation API is Running!"})

@app.route('/create-account', methods=['POST'])
def create_account():
    # For demonstration purpose only
    data = request.json
    username = data.get("username")
    password = data.get("password")
    phone = data.get("phone")

    # Later you will integrate OTPWorld API & Selenium Automation here
    return jsonify({
        "status": "success",
        "message": f"Account created for {username} (Not really, just simulated 😄)"
    })

if __name__ == '__main__':
    app.run(debug=True)
