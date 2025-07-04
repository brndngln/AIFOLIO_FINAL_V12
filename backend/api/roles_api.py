from fastapi import APIRouter, Body
<<<<<<< HEAD
from security.role_manager import set_admin_roles, get_admin_roles, list_admins
=======
from security.role_manager import set_admin_roles, list_admins
>>>>>>> omni_repair_backup_20250704_1335

router = APIRouter()

@router.get('/api/roles/list')
def list_roles():
    return list_admins()

@router.post('/api/roles/set')
def set_roles(data: dict = Body(...)):
    admin_id = data.get('adminId')
    roles = data.get('roles', [])
    set_admin_roles(admin_id, roles)
    return {'success': True, 'adminId': admin_id, 'roles': roles}
