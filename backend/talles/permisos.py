from rest_framework.permissions import BasePermission


class EsAdminTalles(BasePermission):
    """
    Solo los usuarios pertenecientes al grupo 'admin'
    pueden crear, modificar o eliminar talles.
    """

    def has_permission(self, request, view):
        
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return (
            request.user.is_authenticated
            and request.user.groups.filter(name='admin').exists()
        )