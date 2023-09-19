from brightspace_scrapper import Scrapper
from brightspace_scrapper.content import extract_content, sanitize
from concurrent.futures import ThreadPoolExecutor
import json, os
from tqdm import tqdm

scrapper = Scrapper()
courses = scrapper.get_courses()

def process_course(course):
    r = scrapper.get_course_content(course['id'])
    cname = sanitize(course['name'])
    sem = sanitize(course['semester'])
    os.makedirs(f"courses/{sem}/{cname}", exist_ok=True)
    with open(f"courses/{sem}/{cname}/content.json", "w") as f:
        json.dump(r, f, indent=4)
    contentlist = extract_content(r)

    for content in tqdm(contentlist, desc=f"Processing course {course['id']}", leave=False):
        ext = content['url'].split('.')[-1]
        path = "/".join(content['path'])
        filepath = f"courses/{sem}/{cname}/{path}/{content['name']}.{ext}"
        if os.path.exists(filepath):
            continue
        
        os.makedirs(f"courses/{sem}/{cname}/{path}", exist_ok=True)
        r = scrapper.get_content(course['id'], content['url'])

        if len(filepath) > 215:
            filepath = filepath[:210] + "." + ext
        
        with open(filepath, "wb") as f:
            f.write(r)

with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_course, courses)