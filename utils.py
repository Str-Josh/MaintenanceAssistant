import app
from functools import wraps
from flask_login import current_user
from flask import current_app, g


def _is_logged_in_with_confirmed_email(user_manager):
    """| Returns True if user is logged in and has a confirmed email address.
    | Returns False otherwise.
    """
    # User must be logged in
    if user_manager.call_or_get(current_user.is_authenticated):
        # Is unconfirmed email allowed for this view by @allow_unconfirmed_email?
        unconfirmed_email_allowed = \
            getattr(g, '_flask_user_allow_unconfirmed_email', False)
        
        # unconfirmed_email_allowed must be True or
        # User must have at least one confirmed email address
        if unconfirmed_email_allowed or user_manager.db_manager.user_has_confirmed_email(current_user):
            return True

    return False


def roles_required(*role_names):
    """| This decorator ensures that the current user is logged in,
    | and has *all* of the specified roles (AND operation).

    Example::

        @route('/escape')
        @roles_required('Special', 'Agent')
        def escape_capture():  # User must be 'Special' AND 'Agent'
            ...

    | Calls unauthenticated_view() when the user is not logged in
        or when user has not confirmed their email address.
    | Calls unauthorized_view() when the user does not have the required roles.
    | Calls the decorated view otherwise.
    """
    def wrapper(view_function):

        @wraps(view_function)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            user_manager = current_app.user_manager

            # User must be logged in with a confirmed email address
            allowed = _is_logged_in_with_confirmed_email(user_manager)
            if not allowed:
                # Redirect to unauthenticated page
                return user_manager.unauthenticated_view()

            # User must have the required roles
            if not current_user.has_roles(*role_names):
                # Redirect to the unauthorized page
                return user_manager.unauthorized_view()

            # It's OK to call the view
            return view_function(*args, **kwargs)

        return decorator

    return wrapper