import os
import base64
import json
from Library.Stash import Stash
from Library.PullRequest import PullRequest
from Change import Change
import configparser


def get_comments(change, comments_counter, files):
    for file in files:
        #
        change.files.append(file.path.toString)
        change.formats.add(file.path.extension)
        #
        list_of_comments = file.get_comments()
        if len(list_of_comments) > 0:
            comments_counter += len(list_of_comments)
            change.comments_text.append(file.path.name + ": " + str(list_of_comments))

    return [change, comments_counter]

def check(change, _reviewed_, comments_counter, pull_requests):
    if not _reviewed_:
        for pull_request in pull_requests:
            if pull_request.conteins(commit):
                _reviewed_ = True
                change.state = "Reviewed"
                change.reviewed = "True"
                change.review += commit.url.replace("/rest/api/1.0", "")

                for reviewer in pull_request.reviewers:
                    change.reviewers.append(reviewer.name)

                for comment in pull_request.comments:
                    comments_counter += 1
                    change.comments_text.append(str(comment))

                change, comments_counter = get_comments(
                    change, comments_counter, pull_request.get_commit_by_id(commit.id).files()
                )

    return [change, _reviewed_, comments_counter]


ola_gang_num_style = "asdljgiod;fug09eirtelrmgmnknv;gheriljg"

class Start:
    def get_owner(self):
        return "Start::::"
start = Start()


def read_mappings(name_of_file):
    output = {}
    config = configparser.ConfigParser()
    config.sections()
    config.read(name_of_file)
    for key in config['PathRespMapping']:
        output[key] = config['PathRespMapping'][key]
    return output

def replace_domain_by_mapping(name_of_file, changes):
    mappings = read_mappings(name_of_file)
    domains = list()
    for change in changes:
        for file in change.files:
            for mapping in mappings:
                if mapping.lower() in file.lower():
                    if mappings[mapping] not in domains:
                        domains.append(mappings[mapping])
                    break
        change.domain = domains
    return changes


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

    stash = Stash(start, "https://adc.luxoft.com/stash", login, password)

    # ---------- Get All Commits ----------
    # for project in stash.get_all_projects():
    #     for repo in project.get_all_repositories():
    #         print(project.name, ":", repo.name)
    #         for commit in repo.commits():
    #             print(commit.author.name)

    # ---------- Get All Pull Requests ----------
    # project = stash.get_project_by_name("Luxoft Tools")
    # repository = project.get_repository_by_name("iwa")
    #
    # for pull_request in repository.get_all_pull_requests(state="merged"):
    #     pr = PullRequest(stash, repository.url, pull_request)
    #     pr.show()

    # ---------- Get All Commits ----------
    project = stash.get_project_by_name("Luxoft Tools")
    repository = project.get_repository_by_slug("iwa")

    changes = list()

    print(project.name, ":", repository.name)

    # Fetch all information from pull requests
    pull_requests_merged = list()    # reviewed
    pull_requests_open = list()      # under review
    pull_requests_declined = list()  # declined

    for pull_request in repository.get_all_pull_requests(state="merged"):
        pr = PullRequest(start, stash, repository.url, pull_request)
        pull_requests_merged.append(pr)

    for pull_request in repository.get_all_pull_requests(state="open"):
        pr = PullRequest(start, stash, repository.url, pull_request)
        pull_requests_open.append(pr)

    for pull_request in repository.get_all_pull_requests(state="declined"):
        pr = PullRequest(start, stash, repository.url, pull_request)
        pull_requests_declined.append(pr)

    # Fetch all information from commits
    commits = repository.commits()

    for commit in commits:
        if True:
            change = Change(start)

            _reviewed_ = False
            comments_counter = 0
            change.change = commit.id
            change.date = commit.authorTimestamp
            change.author = commit.author.name

            change, _reviewed_, comments_counter = check(change, _reviewed_, comments_counter, pull_requests_merged)
            change, _reviewed_, comments_counter = check(change, _reviewed_, comments_counter, pull_requests_open)
            change, _reviewed_, comments_counter = check(change, _reviewed_, comments_counter, pull_requests_declined)

            if not _reviewed_:
                commit_files = commit.files()
                if len(commit_files) == 0:
                    continue
                change, comments_counter = get_comments(change, comments_counter, commit_files)
            change.comments = comments_counter
            changes.append(change)

    changes = replace_domain_by_mapping('responsibles.ini', changes)

    with open('data.json', 'w') as fp:
        output = list()
        for change in changes:
            output.append(change.to_dict())
        json.dump(output, fp, sort_keys=True, indent=4)
