def list_course_content(scp, course):
    url = f"{scp.config.URL_BASE}/d2l/api/le/unstable/{course}/content/toc?loadDescription=true"
    r = scp.client.get(url, headers = {
        'Authorization': f'Bearer {scp.get_token()}'
    }).json()

    return r

def extract_content(data, path = []):
    l = []
    if 'Modules' in data:
        for module in data['Modules']:
            l += extract_content(module, path + [sanitize(module.get('Title', ''))])
    if 'Topics' in data:
        for topic in data['Topics']:
            if topic['Url'] and topic['Url'].startswith('/content/'):
                l.append({
                    'name': sanitize(topic['Title']),
                    'path': path[:],
                    'url': topic['Url']
                })
    return l
    
def sanitize(s):
    return s.replace('/', '_').replace(':', '_').strip().replace('–', '-')

def get_content(scp, course, url):
    url = f"{scp.config.URL_BASE}/{url}"
    r = scp.client.get(url, data ={
        'd2lSessionVal': scp.client.cookies.get('d2lSessionVal'),
        'ou': course,
        'd2l_body_type': '3',
        'retargetQuicklinks': 'true'
    }).content

    return r