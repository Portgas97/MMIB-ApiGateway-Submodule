from flask_login import UserMixin


class UserAuth(UserMixin):
    """
    This class represents an authenticated user.
    It is not a model, it is only a lightweight class used
    to represents an authenticated user.
    """
    id = None
    email = None
    is_active = None
    is_admin = None
    authenticated = None
    is_anonymous = False
    extra_data = None

    @staticmethod
    def build_from_json(json: dict):
        kw = {key: json[key] for key in ['id', 'email', 'is_active', 'authenticated', 'is_anonymous']}
        extra = json.copy()
        all(map(extra.pop, kw))
        kw['extra'] = extra

        return UserAuth(**kw)

    def __init__(self, **kw):
        self.id = kw["id"]
        self.email = kw["email"]
        self.is_active = kw.get("is_active", True)
        self.authenticated = kw.get("authenticated", True)
        self.is_anonymous = kw.get("is_anonymous", True)
        self.extra_data = kw.get('extra')
        self.firstname = kw['firstname']
        self.is_admin = kw.get('is_admin', False)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def __getattr__(self, item):
        if item in self.__dict__:
            return self[item]
        elif item in self.extra_data:
            return self.extra_data[item]
        else:
            raise AttributeError('Attribute %s does not exist' % item)

    def __str__(self):
        s = 'User Object\n'
        for (key, value) in self.__dict__.items():
            s += "%s=%s\n" % (key, value)
        return s
