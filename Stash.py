import urllib.request
import base64
import json

from Project import Project


class Stash:
    def __init__(self, path_to_stash, login, password):
        self.path_to_stash = self.__correct_path(path_to_stash) + "/rest/api/1.0"
        self.basic = (b"Basic " + base64.b64encode(login.encode()+b":"+password.encode())).decode()

    def rest_request(self, url):
        req = urllib.request.Request(url)
        req.add_header("Authorization", self.basic)
        req.add_header("Content-Type", "application/json")
        return json.loads(urllib.request.urlopen(req).read().decode())

    def get_all_projects(self):
        projects = list()
        for project in self.rest_request(self.path_to_stash + "/projects")['values']:
            projects.append(Project(self, project))
        return projects

    def get_all_pull_requests(self):
        url = self.path_to_stash + "/projects/LUXTOOLS/repos/iwa/pull-requests"
        print(url)
        return self.rest_request(url)

    def get_project_by_name(self, name):
        for project in self.get_all_projects():
            if project.name == name:
                return project
        return None

    def get_project_by_key(self, key):
        for project in self.get_all_projects():
            if project.key == key:
                return project
        return None

    def get_project_by_id(self, id):
        for project in self.get_all_projects():
            if project.id == id:
                return project
        return None
        
    def __correct_path(self, path):
        if '/' == path[-1]:
            path = path[0:-1]
        return path