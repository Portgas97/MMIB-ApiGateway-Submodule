import functools

from flask_login import LoginManager, current_user, login_manager

from mib.auth.userauth import UserAuth
from mib.rao.user_manager import UserManager


def init_login_manager(app):
    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'
    login_manager.refresh_view = 'auth.re_login'

    @login_manager.user_loader
    def load_user(user_id):
        """
        We need to connect to users endpoint and load the user.
        Here we can implement the redis caching

        :param user_id: user id
        :return: the user object
        """
        user = UserManager.get_by_id(user_id)
        if user is None:
            return None
        usrauth = UserAuth(id=user['id'], email=user['email'])
        usrauth.authenticated = True
        return usrauth

    return login_manager

def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required
