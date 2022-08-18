from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from .setup import config, blueprint, login_det, map

db = SQLAlchemy()

def constructor():
    app = Flask(__name__, template_folder = 'templates', static_folder='static')
    config(app)    
    blueprint(app)    
    
    if os.path.exists('app/' + 'tracker.db') == False:
        db.create_all(app=app)
        print('DB Created')
    
    login_det(app)    
    
    map(app)
    
    return app
    
    
    
    




