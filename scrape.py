from brightspace_scrapper import Scrapper
from brightspace_scrapper.content import extract_content, sanitize
import json, os

scrapper = Scrapper()
courses = scrapper.get_courses()


for course in courses:
    r = scrapper.get_course_content(course['id'])
    cname = sanitize(course['name'])
    os.makedirs(f"courses/{cname}", exist_ok=True)
    with open(f"courses/{cname}/content.json", "w") as f:
        json.dump(r, f, indent=4)
    
    for content in extract_content(r):
        print(content)
        ext = content['url'].split('.')[-1]
        path = "/".join(content['path'])
        filepath = f"courses/{cname}/{path}/{content['name']}.{ext}"
        if os.path.exists(filepath):
            continue
        
        os.makedirs(f"courses/{cname}/{path}", exist_ok=True)
        r = scrapper.get_content(course['id'], content['url'])

        if len(filepath) > 215:
            filepath = filepath[:210] + "." + ext
        with open(filepath, "wb") as f:
            f.write(r)