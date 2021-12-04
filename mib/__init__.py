# import re
# from jinja2 import evalcontextfilter
# from markupsafe import Markup, escape
# import datetime
# import sys
import os
from flask import Flask
# from flask_uploads import configure_uploads
from flask_bootstrap import Bootstrap
from flask_environments import Environments

from mib import encoder

"""
from mib.background import LOTTERY_PRICE
from mib.auth import login_manager as lm
from mib.database import User, db
from mib.views import blueprints
from mib.forms import images
from mib.send import UPLOAD_FOLDER, MAX_CONTENT_LENGTH
"""

__version__ = '0.1'

login = None
debug_toolbar = None
app = None


def create_app():
    global app
    global login
    # instance_relative_config=True tells the app that configuration files
    # are relative to the instance folder (it can hold local data that
    # shouldn't be committed to version control, such as configuration
    # secrets and the database file)
    app = Flask(__name__, instance_relative_config=True)

    flask_env = os.getenv('FLASK_ENV', 'None')

    # from mib.send import UPLOAD_FOLDER, MAX_CONTENT_LENGTH --> produce
    # circolar import error (I think)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'SUPER_SECRET'
    # _app.config['UPLOADED_IMAGES_DEST'] = UPLOAD_FOLDER
    # _app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    # now these are set in config.py
    # disable CSRF protection when the app is running in dev or test mode
    # if _app.config['ENV'] == 'development' or "pytest" in sys.modules:
    #    _app.config['WTF_CSRF_ENABLED'] = False
    # if "pytest" in sys.modules:
    #    _app.config['TESTING'] = True
    #    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../T_mmiab.db'
    # else:
    #    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../mmiab.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../mmiab.db'

    if flask_env == 'development':
        config_object = 'config.DevConfig'
    elif flask_env == 'testing':
        config_object = 'config.TestConfig'
    elif flask_env == 'production':
        config_object = 'config.ProdConfig'
    else:
        raise RuntimeError(
            "%s is not recognized as valid app environment. "
            "You have to setup the environment!" % flask_env
        )

    # Load config
    env = Environments(app)
    env.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)
    register_handlers(app)

    import mib.auth as lm
    login = lm.init_login_manager(app)

    if flask_env == 'testing' or flask_env == 'development':
        register_test_blueprints(app)

    # I don't think this is needed anymore
    # configure_uploads(_app, images)
    # for bp in blueprints:
    #    _app.register_blueprint(bp)
    #    bp.app = _app

    # db.init_app(_app)
    # login_manager.init_app(_app)
    # db.create_all(app=_app)

    # create a first admin user
    """
    with _app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.firstname = 'Admin'
            example.lastname = 'Admin'
            example.email = 'example@example.com'
            example.date_of_birth = datetime.datetime(2020, 10, 5)
            example.is_admin = True
            example.content_filter = False
            example.set_password('admin')
            example.set_points(10 * LOTTERY_PRICE)
            db.session.add(example)
            db.session.commit()
    """
    app.json_encoder = encoder.JSONEncoder
    return app



def register_extensions(app):
    """
    It register all extensions
    :param app: Flask Application Object
    :return: None
    """
    global debug_toolbar

    if app.debug:
        try:
            from flask_debugtoolbar import DebugToolbarExtension
            debug_toolbar = DebugToolbarExtension(app)
        except ImportError:
            pass

    # adding bootstrap
    Bootstrap(app)


def register_blueprints(app):
    """
    This function registers all views in the flask application
    :param app: Flask Application Object
    :return: None
    """
    from mib.views import blueprints
    for bp in blueprints:
        app.register_blueprint(bp, url_prefix='/')


def register_test_blueprints(app):
    """
    This function registers the blueprints used only for testing purposes
    :param app: Flask Application Object
    :return: None
    """

    from mib.views.utils import utils
    app.register_blueprint(utils)


def register_handlers(app):
    """
    This function registers all handlers to application
    :param app: application object
    :return: None
    """
    from .handlers import page_404, error_500

    app.register_error_handler(404, page_404)
    app.register_error_handler(500, error_500)


"""
_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                          for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result
"""
