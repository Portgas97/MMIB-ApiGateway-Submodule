import functools

from flask_login import LoginManager, current_user

from mib.database import User

from flask_login import LoginManager
from mib.rao.user_manager import UserManager
from mib.database import User as DBUser



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
        user = User.from_dict(user)
        user = _user2dbuser(user)
        user._authenticated = True
        user.is_active = True
        user.is_anonymous = False
        user.authenticated = True
        return user

    return login_manager


# from here on is OLD CODE
login_manager = LoginManager()


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required


@login_manager.user_loader
def load_user(user_id):
    user = UserManager.get_by_id(user_id)
    if user is None:
        return None
    user = User.from_dict(user)
    user = _user2dbuser(user)
    user._authenticated = True
    user.is_active = True
    user.is_anonymous = False
    user.authenticated = True
    return user

def _user2dbuser(data):
    """
    Convert a User object to a DBUser object
    """
    user = DBUser()
    user.email = data.email
    user.firstname = data.firstname
    user.lastname = data.lastname
    user.set_password(data.password)
    user.date_of_birth = data.date_of_birth
    return user
