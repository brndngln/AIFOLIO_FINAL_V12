from fastapi import APIRouter, Request, Body
from security.role_manager import get_admin_roles
import requests
import os

router = APIRouter()

# Example: OIDC/SAML/Google SSO integration
SSO_PROVIDER_URL = os.environ.get('SSO_PROVIDER_URL')
SSO_CLIENT_ID = os.environ.get('SSO_CLIENT_ID')
SSO_CLIENT_SECRET = os.environ.get('SSO_CLIENT_SECRET')

@router.post('/api/sso/custom_login')
def custom_sso_login(request: Request, data: dict = Body(...)):
    code = data.get('code')
    # Exchange code for token (OIDC/OAuth2)
    token_url = f"{SSO_PROVIDER_URL}/token"
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': SSO_CLIENT_ID,
        'client_secret': SSO_CLIENT_SECRET,
        'redirect_uri': data.get('redirect_uri')
    }
    resp = requests.post(token_url, data=payload)
    if resp.status_code != 200:
        return {'success': False, 'error': 'SSO token exchange failed'}
    token = resp.json().get('access_token')
    # Get user info
    userinfo_url = f"{SSO_PROVIDER_URL}/userinfo"
    headers = {'Authorization': f'Bearer {token}'}
    userinfo = requests.get(userinfo_url, headers=headers).json()
    admin_id = userinfo.get('email', '').split('@')[0]
    roles = get_admin_roles(admin_id)
    if not roles:
        return {'success': False, 'error': 'No roles assigned'}
    return {'success': True, 'adminId': admin_id, 'roles': roles, 'userinfo': userinfo}
