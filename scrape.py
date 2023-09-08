from brightspace_scrapper import Scrapper
from brightspace_scrapper.content import extract_content
import json, os

scrapper = Scrapper()
courses = scrapper.get_courses()


for course in courses:
    r = scrapper.get_course_content(course['id'])
    os.makedirs(f"courses/{course['name']}", exist_ok=True)
    with open(f"courses/{course['name']}/content.json", "w") as f:
        json.dump(r, f, indent=4)
    
    for content in extract_content(r):
        print(content)
        ext = content['url'].split('.')[-1]
        path = "/".join(content['path'])
        if os.path.exists(f"courses/{course['name']}/{path}/{content['name']}.{ext}"):
            continue
        
        os.makedirs(f"courses/{course['name']}/{path}", exist_ok=True)
        r = scrapper.get_content(course['id'], content['url'])

        with open(f"courses/{course['name']}/{path}/{content['name']}.{ext}", "wb") as f:
            f.write(r)