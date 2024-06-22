import base64
from Crypto.Cipher import AES


class Cryptor:
    def __init__(self, password: str):
        password = password.rjust(32)[:32]
        self._cipher = AES.new(password.encode("utf-8"), AES.MODE_ECB)

    def encrypt(self, data: str) -> str:
        if data.startswith(" "):
            raise ValueError("Data should not start with space!")
        return base64.b64encode(self._cipher.encrypt(data.encode("utf-8").rjust(64))).decode("utf-8")

    def decrypt(self, data: str) -> str:
        return self._cipher.decrypt(base64.b64decode(data.encode("utf-8"))).decode("utf-8").lstrip()
