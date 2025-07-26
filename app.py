from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/create-account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Dummy response for now
    return jsonify({
        "status": "success",
        "username": username,
        "password": password,
        "message": "Account creation simulator"
    })

if __name__ == '__main__':
    app.run()
