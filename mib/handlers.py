from flask import render_template


def page_404(e):
    return abort(404)


def error_500(e):
    return abort(500)
