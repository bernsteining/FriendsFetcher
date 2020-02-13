from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import re
import time
import json
import sys
import os
import argparse

parser = argparse.ArgumentParser(
    description=
    "FriendsFetcher, a tool to scrap someone's friends on Facebook.  Usage: python3 FriendsFetcher.py -t <target_account>",
    prog="FriendsFetcher")

parser.add_argument(
    "-t",
    "--target",
    dest="target_account",
    help="Facebook profile to investigate",
)

parser.add_argument(
    "-l",
    "--login",
    dest="login",
    help=
    "Facebook profile to connect to, in order to access the Facebook Profile of the target account",
)

parser.add_argument(
    "-p",
    "--password",
    dest="password",
    help="Password of the Facebook profile to connect to",
)

parser.add_argument(
    "-v",
    "--visual",
    action='store_true',
    help="Spawns Chromium GUI, otherwise Chromium is headless",
)

args = parser.parse_args()


def launch_browser(option):
    if not option:
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        return webdriver.Chrome("/usr/bin/chromedriver",
                                chrome_options=chrome_options)
    else:
        chrome_options = Options()

        return webdriver.Chrome("/usr/bin/chromedriver")


def login(account, password):
    try:
        print(
            "Logging in with " + account + "'s Facebook account ...",
            end="\r",
        )
        browser.get("https://www.facebook.com")
        time.sleep(1)  #find element won't work if this is removed

        login = browser.find_element_by_xpath("//input[@name='email']")
        passwd = browser.find_element_by_xpath("//input[@name='pass']")
        login.send_keys(account)
        passwd.send_keys(password)
        login.submit()
        time.sleep(2)
        browser.get("https://www.facebook.com/" + args.target_account +
                    "/friends")
        return True
    except:
        return False


def scrolls(
    friends_number,
):  # scrolls required to snag all the data accordingly to the number of friends (kind of)
    return (int(friends_number)) // 11


def fetch_friends(number_publications, browser):
    links = []
    webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    links.extend(
        re.findall("facebook.com/([^/]+)?fref=profile_friend_list",
                   browser.page_source))
    n_scrolls = scrolls(number_publications)

    for i in range(n_scrolls):
        print(
            "Scrolling the friendlist ..." + str(100 * i // n_scrolls) +
            "% of the profile scrolled ",
            end="\r",
        )
        browser.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)")
        links.extend(
            re.findall("facebook.com/([^/]+)?fref=profile_friend_list",
                       browser.page_source))
        time.sleep(
            1
        )  # dont change this, otherwise some scrolls won't be effective and all the data won't be scrapped

    return list(dict.fromkeys(links))  # remove duplicates


browser = launch_browser(args.visual)
browser.get("https://www.facebook.com/")
login(args.login, args.password)
friends_number = re.search("class=\"_3d0\">([0-9,]+)</span>",
                           browser.page_source).group(1)
friends = fetch_friends(friends_number, browser)

friends_filtered = []
for friend in friends:
    friends_filtered.append("www.facebook.com/" + friend[:-1])

print(friends_filtered)