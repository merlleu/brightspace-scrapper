from . import courses
from . import config
from . import auth
from . import content
import requests

class Scrapper:
    client = None
    config = config
    csrf = None
    token = None
    def __init__(self) -> None:
        self.client = requests.Session()
        cookies = config.COOKIES
        
        for cookie in cookies.split("; "):
            key, value = cookie.split("=")
            self.client.cookies.set(key.strip(), value.strip())

        self.client.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Referer': 'https://devinci-online.brightspace.com/d2l/home',
            'Origin': 'https://devinci-online.brightspace.com',
        })
        
    def get_courses(self):
        return courses.list_courses(self)
    
    def get_csrf(self):
        if self.csrf is None:
            self.csrf = auth.get_csrf(self)
        return self.csrf
    
    def get_token(self):
        if self.token is None:
            self.token = auth.obtain_token(self)
        return self.token

    def get_course_content(self, course):
        return content.list_course_content(self, course)

    def get_content(self, course, url):
        return content.get_content(self, course, url)