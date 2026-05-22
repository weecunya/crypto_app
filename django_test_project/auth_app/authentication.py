import jwt
from .models import User
from  myproject.settings import JWT_SECRET_KEY


def get_user_from_token(request):

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None

    parts = auth_header.split()
    if len(parts) != 2 or parts[0] != 'Bearer':
        return None

    token = parts[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])

    except jwt.InvalidTokenError:
        return None

    user_id = payload.get('user_id')
    if not user_id:
        return None

    try:
        user = User.objects.get(id=user_id, is_active=True)
        return user
    except User.DoesNotExist:
        return None