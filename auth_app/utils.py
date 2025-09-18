import random
from core.redis_client import r

OTP_EXPIRY = 300  # 5 minutes

#Third-party SMS = OTP delivered to a real phone
#Mocked (Postman) = OTP delivered via API response for testing

def generate_otp():
    return str(random.randint(100000, 999999))

def store_otp(mobile_number, otp):
    r.set(f"otp:{mobile_number}", otp, ex=OTP_EXPIRY)

def verify_otp(mobile_number, otp):
    stored_otp = r.get(f"otp:{mobile_number}")
    if stored_otp and stored_otp.decode() == otp:
        r.delete(f"otp:{mobile_number}")
        return True
    return False
