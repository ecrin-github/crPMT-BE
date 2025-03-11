from users.models import Users


def is_user_admin(email: str) -> bool:
    email_split = email.split('@')
    email_domain = email_split[1]
    if 'ecrin' in email_domain or 'ecrin.org' in email_domain or 'tsd' in email_domain:
        return True
    return False


def is_user_exists(email: str) -> bool:
    return Users.objects.filter(email=email).exists()


def get_user_by_email(email: str):
    return Users.objects.get(email=email)
