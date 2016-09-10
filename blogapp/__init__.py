from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


def authenticate(email=None, password=None):
    UserOwner = get_user_model()
    try:
        user = UserOwner.objects.get(email=email)
    except UserOwner.DoesNotExist:
        # Create a new user. Note that we can set password
        # to anything, because it won't be checked; the password
        # from settings.py will.
        return None

    if user.password == password:
        return user
    if check_password(password, user.password):
        return user
    return None
