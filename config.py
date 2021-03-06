import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True
    GOOGLE_MAPS_API_KEY='AIzaSyBiWsPU8SBOTUQCDWfayIMwUz-dkmRgbcs'
    OPENMAP_API_KEY = 'a5cadd47301964589bcd2ab61301379b'