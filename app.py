from flask import Flask, request, jsonify
import random
import string
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

OTP_API_KEY = "276e8c19b57e05735887644fab6cdeb5"
SERVICE = "winclash"
OTPWORLD_BASE = "https://otpworld.in"

# Generate random Gmail email
def generate_random_email():
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@gmail.com"

# Get phone number from OTPWorld
def get_phone_number():
    url = f"{OTPWORLD_BASE}/api/get_number.php?apikey={OTP_API_KEY}&service={SERVICE}"
    response = requests.get(url)
    data = response.json()
    return data["number"], data["id"]

# Get OTP from OTPWorld
def get_otp(request_id):
    for _ in range(30):
        time.sleep(3)
        url = f"{OTPWORLD_BASE}/api/get_otp.php?apikey={OTP_API_KEY}&requestid={request_id}"
        response = requests.get(url)
        data = response.json()
        if data["Status"] == "Success":
            return data["otp"]
    return None

# Automate Winclash form submission
def create_account_winclash(email, phone):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://winclash.com/join-now")

    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    password = "Test@1234"

    try:
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone").send_keys(phone)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.NAME, "confirm_password").send_keys(password)

        driver.find_element(By.ID, "register-btn").click()
        time.sleep(2)  # Wait for OTP field to appear

        return driver, username, password
    except Exception as e:
        driver.quit()
        return None, None, None

@app.route("/create-account", methods=["POST"])
def create_account():
    email = generate_random_email()
    phone, req_id = get_phone_number()

    driver, username, password = create_account_winclash(email, phone)
    if not driver:
        return jsonify({"error": "Form submission failed"}), 500

    otp = get_otp(req_id)
    if not otp:
        driver.quit()
        return jsonify({"error": "Failed to fetch OTP"}), 500

    try:
        driver.find_element(By.NAME, "otp").send_keys(otp)
        driver.find_element(By.ID, "verify-btn").click()
        time.sleep(2)
        driver.quit()
        return jsonify({
            "status": "success",
            "email": email,
            "phone": phone,
            "username": username,
            "password": password,
            "message": "Account created successfully"
        })
    except Exception as e:
        driver.quit()
        return jsonify({"error": "OTP submission failed"}), 500

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "✅ Winclash Automation API is Running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
