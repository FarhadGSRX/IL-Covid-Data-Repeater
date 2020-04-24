import subprocess as cmd
from datetime import datetime


def the_work():
    the_date_n_time = datetime.now().strftime("%m-%d-%H%M")

    cp = cmd.run("cd /home/pi/Git/NicksNewsUpdater/", check=True, shell=True)
    print(cp)

    cp = cmd.run("git add .", check=True, shell=True)
    print(cp)

    # response = input("Do you want to use the default message for this commit?([y]/n)\n")
    message = "Automatic Update (%s)" % the_date_n_time

    # if response.startswith('n'):
    #    message = input("What message you want?\n")

    cp = cmd.run(f"git commit -m '{message}'", check=True, shell=True)
    cp = cmd.run("git push -u origin master -f", check=True, shell=True)

    print("Git Pushed without error.")
