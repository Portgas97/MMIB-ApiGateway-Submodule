from __future__ import print_function
from flask import Blueprint, abort

import sys

# this is only a utility view
utils = Blueprint('util', __name__)


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@utils.route('/server_error')
def generate_server_error():
    """
    This method will generate an error
    :return: Error 500
    """
    return abort(500)
