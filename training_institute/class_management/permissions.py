from rest_framework.permissions import BasePermission,SAFE_METHODS




class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        
        if request.method in SAFE_METHODS:
            return True

        
        return request.user.role == "admin" or request.user.is_superuser

class MarkPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True

        
        if request.user.role in ["admin", "teacher"]:
            return True

        
        if request.user.role == "student":
            return request.method in SAFE_METHODS

        return False

# class IsTeacher(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "teacher"
    
# class IsStudent(BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.role == "student"



########################
