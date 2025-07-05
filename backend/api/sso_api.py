from fastapi import APIRouter, Body
from security.role_manager import get_admin_roles

router = APIRouter()


# This is a placeholder for real SSO integration (e.g., SAML/OIDC/Google)
@router.post("/api/sso/login")
def sso_login(data: dict = Body(...)):
    email = data.get("email")
    # In a real app, validate SSO token/assertion here
    # For demo, accept any email and map to adminId
    admin_id = email.split("@")[0]
    roles = get_admin_roles(admin_id)
    if not roles:
        return {"success": False, "error": "No roles assigned"}
    return {"success": True, "adminId": admin_id, "roles": roles}
