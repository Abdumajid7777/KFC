from rest_framework import permissions


class IsReviewOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

    
class IsRestaurantOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'restaurant'):
            return obj.restaurant.owner == request.user
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
            
        return False