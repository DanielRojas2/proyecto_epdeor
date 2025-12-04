from django import template

register = template.Library()

@register.filter
def tiene_rol(usuario, roles):
    """
    roles: lista de roles como string separados por comas
    Ej: "sisadmin,jefe gerencia,jefe jdaf"
    """
    if not usuario.is_authenticated or not hasattr(usuario, "personal"):
        return False

    roles_usuario = set(usuario.personal.cargo.rol.values_list("rol", flat=True))
    roles_check = set([r.strip() for r in roles.split(",")])

    return bool(roles_usuario & roles_check)
