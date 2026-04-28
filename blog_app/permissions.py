from rest_framework.permissions import BasePermission 
# BasePermission - To create custom permission classes
# DRF provides built-in permissions like: IsAuthenticated, AllowAny

# Creating a custom permission class 
# IsAuthor → Only author can modify
# ReadOnly → Others can only read
# Use when you want owner based access control
class IsAuthorOrReadOnly(BasePermission):
     
    # A special method used for object-level permissions
    # Global Permission	has_permission()
    # Object Permission	has_object_permission()
    def has_object_permission(self, request, view, obj):
        
        # Allow read-only methods for everyone
        # GET	Read data
        # HEAD	Metadata
        # OPTIONS	API info
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Only author can edit/delete
        return obj.author == request.user