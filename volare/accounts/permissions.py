from rest_framework.permissions import BasePermission
from accounts.Models.account import AccountRole  # Adjust import based on your structure

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == AccountRole.ADMIN

class IsAdminOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [AccountRole.ADMIN, AccountRole.CUSTOMER]