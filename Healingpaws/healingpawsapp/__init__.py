from flask import Flask
from sqlalchemy import create_engine
import base64
from Crypto.Cipher import AES
from urllib import parse

from healingpawsapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_,and_
from flask_babel import Babel
from werkzeug import ImmutableDict
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
babel = Babel(app)


AES_SECRET_KEY = 'oJ+yi2AhJcHD!7Q0'  # 此处16|24|32个字符
IV = "UfE-Bi=@ezSug#Lu"

# padding算法
BS = len(AES_SECRET_KEY)
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1:])]


class AES_ENCRYPT(object):
    def __init__(self):
        self.key = AES_SECRET_KEY
        self.mode = AES.MODE_CBC

    # 加密函数
    def encrypt(self, text):
        cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext)

    # 解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text)


#engine = create_engine(db, echo=True)
#self.conn = engine.connect()

from healingpawsapp import routes, models

