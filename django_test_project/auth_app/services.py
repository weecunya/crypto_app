import hashlib
import secrets
from auth_app.models import UserRole, Resource, Permission


def hash_password(password:str) -> str:
    salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(),100000)
    return f"{salt}${hash_obj.hex()}"

def check_password(plain:str,hashed:str) -> bool:
    salt, hash_val = hashed.split('$')
    new_hash = hashlib.pbkdf2_hmac('sha256', plain.encode(), salt.encode(), 100000).hex()
    return new_hash == hash_val

def has_permission(user, resource_name:str, operation:str) -> bool:
    if not user:
        return False
    user_roles = UserRole.objects.filter(user=user).values_list('role_id', flat=True)
    try:
        resource = Resource.objects.get(name=resource_name)
    except Resource.DoesNotExist:
        return False
    for role_id in user_roles:
        if Permission.objects.filter(role_id=role_id,**{f'can_{operation}':True}).exists():
                return True
    return False