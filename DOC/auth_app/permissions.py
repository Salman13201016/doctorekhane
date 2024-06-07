from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False    

class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "admin" or request.user.is_superuser:
            return True
        else:
            return False
     
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "doctor" or request.user.role == "admin" or request.user.is_superuser:
            return True
        else:
            return False
        
class IsHospital(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "hospital" or request.user.role == "admin" or request.user.is_superuser:
            return True
        else:
            return False
        
class IsAmbulance(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == "ambulance" or request.user.role == "admin" or request.user.is_superuser:
            return True
        else:
            return False