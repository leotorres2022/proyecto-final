from rest_framework.permissions import BasePermission

class IsAdminUserOrGroup(BasePermission):
     def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser or 
            request.user.groups.filter(name='admin').exists()
        )


class IsAdminOrCreateAuthenticated(BasePermission):
    """Permiso que permite a cualquier usuario autenticado realizar POST (crear).
    Para otros métodos requiere que el usuario sea superusuario o miembro del grupo 'admin'.
    """
    def has_permission(self, request, view):
       
        if request.method == 'POST': #para crear cualquier usuario autenticado
            return bool(request.user and request.user.is_authenticated)

        if not request.user or not request.user.is_authenticated: #para otros metodos ser admin
            return False
        return (
            request.user.is_superuser or
            request.user.groups.filter(name='admin').exists()
        )