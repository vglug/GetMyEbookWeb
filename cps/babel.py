from babel import negotiate_locale
from flask_babel import Babel, Locale
from babel.core import UnknownLocaleError
from flask import request
from .cw_login import current_user

from . import logger

log = logger.create()

babel = Babel()


def get_locale(locale=None):
    # if a user is logged in, use the locale from the user settings
    if current_user is not None and hasattr(current_user, "locale"):
        # if the account is the guest account bypass the config lang settings
        if current_user.name != 'Guest':
            return current_user.locale
    locale_value = None
    if locale:
        locale_value = locale
    else:
        request_locale = request.cookies.get("get_my_ebook_locale")
        user_locale = [request_locale] if request_locale else None
        preferred = list()
        if request.accept_languages:
            for x in request.accept_languages.values():
                try:
                    preferred.append(str(Locale.parse(x.replace('-', '_'))))
                except (UnknownLocaleError, ValueError) as e:
                    log.debug('Could not parse locale "%s": %s', x, e)
        locale_value = negotiate_locale(user_locale or preferred or ['el'], get_available_translations())
    print("Current Locale", locale_value)
    return locale_value


def get_user_locale_language(user_language):
    return Locale.parse(user_language).get_language_name(get_locale())


def get_available_locale():
    return [Locale('en')] + babel.list_translations()


def get_available_translations():
    return set(str(item) for item in get_available_locale())
