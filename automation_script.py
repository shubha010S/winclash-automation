import requests

def get_number_from_otpworld(api_key):
    response = requests.get(f"https://otpworld.pro/api/get_number?key={api_key}&service=winclash&country=bd")
    return response.json()

def get_otp_from_otpworld(api_key, number_id):
    for _ in range(10):
        otp_response = requests.get(f"https://otpworld.pro/api/get_sms?key={api_key}&id={number_id}")
        data = otp_response.json()
        if data["status"] == "success":
            return data["sms"]
        import time; time.sleep(5)
    return None

def create_winclash_account(username, password):
    # STEP 1: Number from OTPWorld
    otp_key = "276e8c19b57e05735887644fab6cdeb5"
    number_data = get_number_from_otpworld(otp_key)
    number = number_data['number']
    number_id = number_data['id']

    # STEP 2: Send OTP from Winclash (you need to automate this step with selenium or requests)

    # STEP 3: Get OTP
    otp = get_otp_from_otpworld(otp_key, number_id)

    # STEP 4: Final Signup (fake here, real you automate with selenium)
    if otp:
        return {"status": "success", "number": number, "otp": otp}
    else:
        return {"status": "failed", "reason": "OTP not received"}
