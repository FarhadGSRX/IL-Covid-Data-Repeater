import subprocess as cmd
from datetime import datetime

'''Assumes git credentials are stored'''

def the_work(script_folder, **kwargs):
    the_date_n_time = datetime.now().strftime("%m-%d-%H%M")

    sf = str(script_folder)
    print(sf)
    print("Running: cd %s" % sf)
    cp = cmd.run("cd %s" % sf, check=True, shell=True)
    print(cp)

    cp = cmd.run("git add .", check=True, shell=True)
    print(cp)

    message = "Automatic Update (%s)" % the_date_n_time

    cp = cmd.run(f"git commit -m '{message}'", check=True, shell=True)
    cp = cmd.run("git push -u origin master -f", check=True, shell=True)

    print("Git Pushed without error.")
