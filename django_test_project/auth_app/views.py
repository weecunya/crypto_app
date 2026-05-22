
# Create your views here.
import hashlib
import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from myproject.settings import JWT_EXPIRATION_SECONDS
from .models import Role,User,UserRole,Permission,Resource


def hash_password(password):
    return hashlib.pbkdf2_hmac('sha256',password.encode(),b'salt',100000).hex()

def check_password(password,password_hash):
    return hash_password(password) == password_hash


def has_permission(user, resource_name, operation):
    if user is None:
        return False
    print(resource_name, operation)
    print(user,user.first_name,user.last_name)
    user_roles = UserRole.objects.filter(user=user).values_list('role', flat=True)
    for role_id in user_roles:
        try:
            resource = Resource.objects.get(name=resource_name)
            perm = Permission.objects.get(role=role_id, resource=resource)
            if operation == 'read' and perm.can_read:
                return True
            if operation == 'write' and perm.can_write:
                return True
            if operation == 'delete' and perm.can_delete:
                return True
        except (Resource.DoesNotExist, Permission.DoesNotExist):
            continue
        return False




@csrf_exempt
@require_http_methods(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error':'invalid json'}, status=400)
    email = data.get('email')
    password = data.get('password')
    password2 = data.get('password2')
    if not email or not password:
        return JsonResponse({'error':'email or password is required'}, status=400)
    if password != password2:
        return JsonResponse({'error':'password is not match'}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error':'email already exists'}, status=400)
    user = User.objects.create(email=email,password_hash=hash_password(password),
first_name=data.get('first_name',''),last_name=data.get('last_name'),patronymic=data.get('patronymic',''))
    default_role = Role.objects.get(name='user')
    UserRole.objects.create(user=user,role=default_role)
    return JsonResponse({'success':'user created'}, status=201)

@csrf_exempt
@require_http_methods(['POST'])
def login(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error':'invalid json'}, status=400)
    email = data.get('email')
    password = data.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse({'error':'user does not exist'}, status=401)
    if not user.is_active:
        return JsonResponse({'error':'user account is disabled'}, status=401)
    if not check_password(password,user.password_hash):
        return JsonResponse({'error':'invalid email or password'}, status=401)
    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(JWT_EXPIRATION_SECONDS)),
    }
    token = jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm='HS256')
    return JsonResponse({'access_token': token})


@require_http_methods(['GET'])
def profile(request):
    if not request.user:
        return JsonResponse({'error':'user does not exist'}, status=401)
    return JsonResponse({
        'id': request.user.id,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'patronymic': request.user.patronymic,
        'is_active': request.user.is_active,
        'created_at': request.user.created_at
    })


@csrf_exempt
@require_http_methods(['PUT'])
def update_profile(request):
    if not request.user:
        return JsonResponse({'error':'user does not exist'}, status=401)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error':'invalid json'}, status=401)
    if 'first_name' in data:
        request.user.first_name = data['first_name']
    if 'last_name' in data:
        request.user.last_name = data['last_name']
    if 'patronymic' in data:
        request.user.patronymic = data['patronymic']
    request.user.save()
    return JsonResponse({'success':'user updated'})


@csrf_exempt
@require_http_methods(['DELETE'])
def delete_profile(request):
    if not request.user:
        return JsonResponse({'error':'user does not exist'}, status=401)
    request.user.is_active = False
    request.user.save()
    return JsonResponse({'success':'user deleted'},status=200)



MOCK_PROJECTS = [
    {'id': 1,'name': ' project_alpha', 'status': 'developing'},
    {'id': 2,'name': ' project_beta', 'status': 'developing'},
    { 'id': 3,'name': ' project_c', 'status': 'ended'},
]


@require_http_methods(['GET'])
def projects_list(request):
    if not request.user:
        return JsonResponse({'error':'user does not exist'}, status=401)
    if not has_permission(request.user,'project_list', "read"): #read
        return JsonResponse({'error':'user does not have permission'}, status=401)
    return JsonResponse({"projects": MOCK_PROJECTS})

@csrf_exempt
@require_http_methods(['POST'])
def create_project(request):
    if not request.user:
        return JsonResponse({'error':'user does not exist'}, status=401)
    print(has_permission(request.user,'project_list',"write"))
    if not has_permission(request.user,'project_list',"write"): #write
        return JsonResponse({'error':'user does not have permission'}, status=403)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error':'invalid json'}, status=400)
    new_id = max(p['id'] for p in MOCK_PROJECTS)+1 if MOCK_PROJECTS else 1
    if not data.get('name') or not data.get('status'):
        return JsonResponse({'error':'invalid json'}, status=400)
    new_project = {'id': new_id, 'name': data.get('name'), 'status': data.get('status')}
    MOCK_PROJECTS.append(new_project)
    return JsonResponse({'success':'project created'},status=201)

@csrf_exempt
@require_http_methods(['DELETE'])
def delete_project(request,project_id):
    if not request.user:
        return JsonResponse({'error':'user does not exist'}, status=401)
    if not has_permission(request.user,'project_list',"delete"):  #delete
        return JsonResponse({'error':'user does not have permission'}, status=403)
    project_to_delete = None
    for p in MOCK_PROJECTS:
        if p['id'] == project_id:
            project_to_delete = p
            break
    if not project_to_delete:
        return JsonResponse({'error':'project not found'}, status=404)
    MOCK_PROJECTS.remove(project_to_delete)
    return JsonResponse({'success':'project deleted'})

@require_http_methods(['GET'])
def admin_users_list(request):
    if not request.user:
        return JsonResponse({"error":"user does not exist"}, status=401)
    if not request.user.is_active:
        return JsonResponse({"error":"user is deleted"}, status=401)
    if not has_permission(request.user,'project_list',"read"): #read
        return JsonResponse({"error":"user does not have permission"}, status=403)
    users = list(User.objects.all().values('id','email','first_name','last_name','is_active'))
    if not users:
        return JsonResponse({"status":"no users yet"}, status=200)
    return JsonResponse({"users": users })

@csrf_exempt
@require_http_methods(['PUT'])
def admin_change_role(request, user_id):
    if not request.user:
        return JsonResponse({"error":"user does not exist"}, status=401)
    if not has_permission(request.user,'project_list',"write"): #write
        return JsonResponse({"error":"user does not have permission"}, status=403)
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error":"invalid json"}, status=400)
    role_name = data.get('role_name')
    if not role_name:
        return JsonResponse({"error":"role name missing"}, status=400)
    try:
        target_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error":"user does not exist"}, status=404)
    try:
        new_role = Role.objects.get(name=role_name)
    except Role.DoesNotExist:
        return JsonResponse({"error":"role does not exist"}, status=404)
    UserRole.objects.filter(user=target_user).delete()
    UserRole.objects.create(user=target_user,role=new_role)
    return JsonResponse({"success":"role updated"})










