from rest_framework.permissions import BasePermission
from .services import has_permission

class HasResourcePermission(BasePermission):
    def __init__(self,resource_name:str,operation:str):
        self.resource_name = resource_name
        self.operation = operation
    def has_permission(self,request,view):
        return has_permission(request.user,self.resource_name,self.operation)

class CanReadProjects(HasResourcePermission):
    def __init__(self):
        super().__init__('project_list','can_read')

class CanWriteProjects(HasResourcePermission):
    def __init__(self):
        super().__init__('project_list','can_write')

class CanDeleteProjects(HasResourcePermission):
    def __init__(self):
        super().__init__('project_list','can_delete')