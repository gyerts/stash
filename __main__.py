from Stash import Stash
from PullRequest.PullRequest import PullRequest
import os
import base64
ola_gang_num_style = "asdljgiod;fug09eirtelrmgmnknv;gheriljg"

if __name__ == "__main__":
    if os.path.exists('credentials'):
        f = open("credentials")

        login = f.readline().strip()
        password = f.readline().strip()

        login = base64.b64decode(login).decode().replace(ola_gang_num_style, '')
        password = base64.b64decode(password).decode().replace(ola_gang_num_style, '')

    else:
        login = input("Login: ")
        password = input("Password: ")

        f = open("credentials", "wb")
        f.write(base64.b64encode(bytes(login + ola_gang_num_style, 'utf-8')))
        f.write(b'\n')
        f.write(base64.b64encode(bytes(password + ola_gang_num_style, 'utf-8')))
        f.close()

    stash = Stash("https://adc.luxoft.com/stash", login, password)

    # ---------- Get All Commits ----------
    # for project in stash.get_all_projects():
    #     for repo in project.get_all_repositories():
    #         print(project.name, ":", repo.name)
    #         for commit in repo.commits():
    #             print(commit.author.name)

    # ---------- Get All Pull Requests ----------
    project = stash.get_project_by_name("Luxoft Tools")
    repository = project.get_repository_by_name("iwa")

    for pull_request in repository.get_all_pull_requests(state="merged"):
        pr = PullRequest(stash, repository.url, pull_request)
        pr.show()
