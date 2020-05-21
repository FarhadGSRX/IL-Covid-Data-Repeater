# Command Line Options

Legacy options to fit Farhad's workflow
* `--rpi`: running on Farhad's raspberry pi? sets vars appropriately
* `--farhadlocal`: running on Farhad's local machine?  sets vars appropriately
* `--notnow`: don't run the program immediately
* `--future`: keep running indefinitely at :15 and :45 past the hour


# Running on Farhad's Machine

After pushing to the main Git branch, here are the steps:

Turn on RPi and get to terminal

```shell script
cd NicksNewsUpdater folder
git fetch --all
git reset --hard origin/master
python3 main.py --rpi --notnow --future
```

# Running elsewhere

```shell script
python main.py
```