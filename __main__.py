from Stash import Stash
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
    print(stash.get_all_pull_requests())
