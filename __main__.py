import os
import base64
import json
from Library.Stash import Stash
from Library.PullRequest import PullRequest
from Change import Change
import configparser
from report_generator_lib.report_views.stash_report_view import stash_report_view

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

def check(change, _reviewed_, comments_counter, pull_requests, commit):
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


def generate_stash_review_report(path_to_stash, project_name, repo_slug, responsibilities_ini, file_output):
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

    stash = Stash(start, path_to_stash, login, password)

    # ---------- Get All Commits ----------
    project = stash.get_project_by_name(project_name)
    repository = project.get_repository_by_slug(repo_slug)

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

            change, _reviewed_, comments_counter = \
                check(change, _reviewed_, comments_counter, pull_requests_merged, commit)

            change, _reviewed_, comments_counter = \
                check(change, _reviewed_, comments_counter, pull_requests_open, commit)

            change, _reviewed_, comments_counter = \
                check(change, _reviewed_, comments_counter, pull_requests_declined, commit)

            if not _reviewed_:
                commit_files = commit.files()
                if len(commit_files) == 0:
                    continue
                change, comments_counter = get_comments(change, comments_counter, commit_files)
            change.comments = comments_counter
            changes.append(change)

    changes = replace_domain_by_mapping(responsibilities_ini, changes)
    output = list()
    for change in changes:
        output.append(change.to_dict())
    stash_report_view(output, file_output)


if __name__ == "__main__":
    generate_stash_review_report(path_to_stash="https://adc.luxoft.com/stash",
                                 responsibilities_ini="responsibles.ini",
                                 project_name="Luxoft Tools",
                                 repo_slug="unified-integration-tooling",
                                 file_output="output.xlsx"
                                 )
