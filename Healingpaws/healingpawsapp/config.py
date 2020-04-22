import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://healingpaws:4tYZ8NPRbi3j7JZM@healingpaws.top/healingpaws'
    # 123456
#mysql -u healingpaws -p4tYZ8NPRbi3j7JZM -h healingpaws.top -P 3306 -D healingpaws
    #SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://healingpaws:4a47475b60356cbc@localhost:3306/healingpaws' #跑不了。。。。。。

    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'mydb.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CV_UPLOAD_DIR = os.path.join(basedir, 'uploaded_CV')

    # PHOTO_UPLOAD_DIR = os.path.join(basedir, 'uploaded_PHOTO')

    PHOTO_UPLOAD_DIR = os.path.join(basedir, 'static/uploaded_PHOTO')


