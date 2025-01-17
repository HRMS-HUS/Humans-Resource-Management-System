import pyotp

def create_otp():
    return pyotp.TOTP(pyotp.random_base32(), interval=600).now()
    
