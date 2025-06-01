from rest_framework.permissions import BasePermission
from accounts.models.account import AccountRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == AccountRole.ADMIN.value


class IsAdminOrCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [AccountRole.ADMIN.value, AccountRole.CUSTOMER.value, AccountRole.COMPANY_ADMIN.value]


class IsCompanyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == AccountRole.COMPANY_ADMIN.value


class IsAnyAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [AccountRole.ADMIN.value, AccountRole.COMPANY_ADMIN.value]