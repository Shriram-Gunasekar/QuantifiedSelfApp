#config

def config(app):
    from . import db
    app.config['SECRET_KEY'] = 'poiuytrewqmnbvcxz'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
    app.config['CSRF_ENABLED'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    app.config['MAX_CONTENT_LENGTH'] = None
    app.config['TEMPLATES_AUTO_RELOAD'] = None
    db.init_app(app)


def map(app):
    app.url_map.strict_slashes = False
    
def blueprint(app):
    
    #Imports
    from .views import views
    from .sign import sign
    
    #Register Blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(sign, url_prefix='/')
    
    #parent = Blueprint('sign', __name__, url_prefix='/sign', template_folder='templates')
    #child = Blueprint('child', __name__, url_prefix='/views')
    #parent.register_blueprint(views, url_prefix='/')
    #app.register_blueprint(sign, url_prefix='/sign')

    
def login_det(app):
    from flask_login import LoginManager
    
    login_manager = LoginManager()
    login_manager.login_view = 'sign.login'
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    
    from .models import Account
    
    @login_manager.user_loader
    def load_user(id):
        return Account.query.get(int(id))
    

    