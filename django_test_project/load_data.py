import os
import django
import hashlib


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from auth_app.models import User, Role, Resource, Permission, UserRole

def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000).hex()


admin_role, _ = Role.objects.get_or_create(name='admin')
user_role, _ = Role.objects.get_or_create(name='user')
print("roles created")

for res_name in ['profile', 'project_list', 'user_permissions']:
    Resource.objects.get_or_create(name=res_name)
print("resources created")

project_res = Resource.objects.get(name='project_list')
Permission.objects.get_or_create(
    role=user_role,
    resource=project_res,
    defaults={'can_read': True, 'can_write': False, 'can_delete': False}
)
Permission.objects.get_or_create(
    role=admin_role,
    resource=project_res,
    defaults={'can_read': True, 'can_write': True, 'can_delete': True}
)
print("permissions created")

user, created = User.objects.get_or_create(
    email='user@example.com',
    defaults={
        'password_hash': hash_password('123'),
        'first_name': 'Обычный',
        'last_name': 'Пользователь',
        'is_active': True
    }
)
if created:
    UserRole.objects.create(user=user, role=user_role)
    print("created user user@example.com / 123")

admin, created = User.objects.get_or_create(
    email='admin@example.com',
    defaults={
        'password_hash': hash_password('admin123'),
        'first_name': 'Админ',
        'last_name': 'Системы',
        'is_active': True
    }
)
if created:
    UserRole.objects.create(user=admin, role=admin_role)
    print("created admin admin@example.com / admin123")

print("created")

