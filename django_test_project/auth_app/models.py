from django.db import models

# Create your models here.


class User(models.Model):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_authenticated(self):
        return True

    @property
    def has_module_perms(self):
        return False

    @property
    def is_anonymous(self):
        return True

    @property
    def has_perm(self):
        return False

    @property
    def is_staff(self):
        return False

    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=225)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100,blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Role(models.Model):
    name = models.CharField(max_length=100,unique=True)

class Resource(models.Model):
    name = models.CharField(max_length=100,unique=True)

class Permission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource,on_delete=models.CASCADE)
    can_read = models.BooleanField(default=False)
    can_write = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

class UserRole(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)