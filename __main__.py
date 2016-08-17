from Stash import Stash
from PullRequest.PullRequest import PullRequest
from Change import Change
import os
import base64


ola_gang_num_style = "asdljgiod;fug09eirtelrmgmnknv;gheriljg"

class Start:
    def get_owner(self):
        return "Start::::"
start = Start()

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

            if not _reviewed_:
                for pull_request in pull_requests_merged:
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
                        for file in pull_request.get_commit_by_id(commit.id).files():
                            #
                            change.files.append(file.path.toString)
                            change.formats.add(file.path.extension)
                            #
                            list_of_comments = file.get_comments()
                            if len(list_of_comments) > 0:
                                comments_counter += len(list_of_comments)
                                change.comments_text.append(file.path.name + ": " + str(list_of_comments))

            if not _reviewed_:
                for pull_request in pull_requests_open:
                    if pull_request.conteins(commit):
                        _reviewed_ = True
                        change.state = "Under review"
                        change.reviewed = "False"
                        change.review += commit.url.replace("/rest/api/1.0", "")

                        for comment in pull_request.comments:
                            comments_counter += 1
                            change.comments_text.append(str(comment))
                        for file in pull_request.get_commit_by_id(commit.id).files:
                            #
                            change.files.append(file.path.toString)
                            change.formats.add(file.path.extension)
                            #
                            list_of_comments = file.get_comments()
                            if len(list_of_comments) > 0:
                                comments_counter += len(list_of_comments)
                                change.comments_text.append(file.path.name + ": " + str(list_of_comments))

            if not _reviewed_:
                for pull_request in pull_requests_declined:
                    if pull_request.conteins(commit):
                        _reviewed_ = True
                        change.state = "Declined"
                        change.reviewed = "True"
                        change.review += commit.url.replace("/rest/api/1.0", "")

                        for reviewer in pull_request.reviewers:
                            change.reviewers.append(reviewer.name)
                        for comment in pull_request.comments:
                            comments_counter += 1
                            change.comments_text.append(str(comment))
                        for file in pull_request.get_commit_by_id(commit.id).files:
                            #
                            change.files.append(file.path.toString)
                            change.formats.add(file.path.extension)
                            #
                            list_of_comments = file.get_comments()
                            if len(list_of_comments) > 0:
                                comments_counter += len(list_of_comments)
                                change.comments_text.append(file.path.name + ": " + str(list_of_comments))

            if not _reviewed_:
                commit_files = commit.files()
                if len(commit_files) == 0:
                    break

                for file in commit_files:
                    #
                    change.files.append(file.path.toString)
                    change.formats.add(file.path.extension)
                    #
                    list_of_comments = file.get_comments()
                    if len(list_of_comments) > 0:
                        comments_counter += len(list_of_comments)
                        change.comments_text.append(file.path.name + ": " + str(list_of_comments))

            change.comments = comments_counter

            changes.append(change)

    for change in changes:
        print('\n\n')
        change.show()
