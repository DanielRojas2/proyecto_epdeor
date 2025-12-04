from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(*roles):
    """
    Decorador para proteger vistas según roles permitidos.
    Ejemplo de uso:
    @role_required("Administrador", "Jefe de Almacén")
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            if not hasattr(request.user, "personal"):
                raise PermissionDenied("El usuario no tiene un Personal asociado")

            personal = request.user.personal

            roles_usuario = personal.cargo.rol.values_list("rol", flat=True)

            if not any(r in roles_usuario for r in roles):
                raise PermissionDenied("No tienes permisos para acceder a esta vista")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
