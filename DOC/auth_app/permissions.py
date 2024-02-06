from rest_framework.permissions import BasePermission

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.profile.role == "admin" or request.user.is_superuser:
            return True
        else:
            return False

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False        
        
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.profile.role == "doctor":
            return True
        else:
            return False
        
class IsHospital(BasePermission):
    def has_permission(self, request, view):
        if request.user.profile.role == "hospital":
            return True
        else:
            return False