import sys
import base64
from Crypto.Cipher import AES
import sys
from django.conf import settings

_aes_key = settings.AES_KEY
_aes_iv = settings.AES_IV

class AESCipher(object):
    def __init__(self, key=_aes_key):
        self.bs = 16
        self.key = key
        
    def encrypt(self, raw, iv=_aes_iv):
        raw = self._pad(raw)
        cipher = AES.new(self.key.encode(), AES.MODE_CBC, iv.encode())
        encrypted = cipher.encrypt(raw.encode())
        encoded = base64.b64encode(encrypted)
        return str(encoded, 'utf-8')

    # def decrypt(self, raw):
    #     decoded = base64.b64decode(raw)
    #     decrypted = self.cipher.decrypt(decoded)
    #     return str(self._unpad(decrypted), 'utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
