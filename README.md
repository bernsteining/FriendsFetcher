# FriendsFetcher
Tool to scrap friends on a Facebook profile.

## Usage:

python3 FriendsFetcher.py -h
usage: FriendsFetcher [-h] [-t TARGET_ACCOUNT] [-l LOGIN] [-p PASSWORD] [-v]

FriendsFetcher, a tool to scrap someone's friends on Facebook. Usage: python3
FriendsFetcher.py -t <target_account>

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_ACCOUNT, --target TARGET_ACCOUNT
                        Facebook profile to investigate
  -l LOGIN, --login LOGIN
                        Facebook profile to connect to, in order to access the
                        Facebook Profile of the target account
  -p PASSWORD, --password PASSWORD
                        Password of the Facebook profile to connect to
  -v, --visual          Spawns Chromium GUI, otherwise Chromium is headless
