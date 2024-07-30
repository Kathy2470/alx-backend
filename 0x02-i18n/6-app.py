#!/usr/bin/env python3
"""
Flask app with Babel configuration, locale selector, and user login emulation.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """
    Configuration class for Flask app.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Determine the best match with our supported languages,
    or force locale from URL, user settings, or request header.
    """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale

    if g.user:
        user_locale = g.user.get('locale')
        if user_locale in app.config['LANGUAGES']:
            return user_locale

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """
    Get user from the users dictionary based on the login_as parameter.
    """
    try:
        user_id = int(request.args.get('login_as'))
        return users.get(user_id)
    except (TypeError, ValueError):
        return None


@app.before_request
def before_request():
    """
    Function to be executed before each request to set the global user.
    """
    g.user = get_user()


@app.route('/')
def index():
    """
    Route for the index page.
    """
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
