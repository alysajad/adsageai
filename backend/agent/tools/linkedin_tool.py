import requests

def post_to_linkedin(text, access_token, urn, visibility='PUBLIC'):
    """
    Posts a text-only update to LinkedIn.
    """
    if not access_token or not urn:
        return {"error": "Missing Access Token or User URN. Please connect LinkedIn first."}

    url = "https://api.linkedin.com/v2/ugcPosts"
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    post_data = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": visibility
        }
    }

    try:
        response = requests.post(url, headers=headers, json=post_data)
        
        if response.status_code in [200, 201]:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False, 
                "status_code": response.status_code, 
                "error": response.text
            }
            
    except Exception as e:
        return {"success": False, "error": str(e)}
