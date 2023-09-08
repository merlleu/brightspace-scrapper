def get_csrf(scp):
    url = f"{scp.config.URL_BASE}/d2l/le/manageCourses/search/{scp.config.UNKNOWN_1}"
    
    r = scp.client.get(url).text
    # extract token: 
    # localStorage.setItem('XSRF.Token','${token}')
    
    token = r.split("localStorage.setItem('XSRF.Token','")[1].split("'")[0]
    return token

def obtain_token(scp):
    url = f"{scp.config.URL_BASE}/d2l/lp/auth/oauth2/token"
    token = scp.client.post(url, data={
        "scope": "*:*:*"
    }, headers = {
        'X-Csrf-Token': scp.get_csrf(),
    }).json()["access_token"]

    return token
