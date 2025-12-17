import os
import requests
import urllib.parse

def get_linkedin_auth_url():
    """
    Generates the LinkedIn OAuth 2.0 authorization URL.
    """
    client_id = os.environ.get('LINKEDIN_CLIENT_ID')
    redirect_uri = os.environ.get('LINKEDIN_REDIRECT_URI')
    
    if not client_id or not redirect_uri:
        raise ValueError("Missing LINKEDIN_CLIENT_ID or LINKEDIN_REDIRECT_URI in environment variables.")

    base_url = "https://www.linkedin.com/oauth/v2/authorization"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": "openid profile w_member_social",
        "state": "random_auth_state_string" # In prod, use CSRF token
    }
    
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def exchange_code_for_token(authorization_code):
    """
    Exchanges the authorization code for an access token.
    """
    client_id = os.environ.get('LINKEDIN_CLIENT_ID')
    client_secret = os.environ.get('LINKEDIN_CLIENT_SECRET')
    redirect_uri = os.environ.get('LINKEDIN_REDIRECT_URI')

    if not all([client_id, client_secret, redirect_uri]):
        raise ValueError("Missing LinkedIn credentials in environment variables.")

    url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get token: {response.text}")

def get_user_info(access_token):
    """
    Fetches basic user info to get the URN (sub).
    """
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch user info: {response.text}")
