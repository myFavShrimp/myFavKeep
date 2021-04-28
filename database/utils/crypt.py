import bcrypt


def encode_pw(password: str):
    hashed = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    return hashed


def check_pw(password: str, hashed):
    return bcrypt.checkpw(password.encode('utf8'), hashed)
