from selenium import webdriver
import time
from pythonbot.secret1.pw import email, password
import pandas as pd


class Instabot:
    def __init__(self, user, password):
        self.data = {}
        self.user = user
        self.password = password
        self.driver = webdriver.Chrome()
        self.driver.get('https://www.instagram.com/')
        time.sleep(2)
        username = self.driver.find_element_by_xpath("//input[@name=\"username\"]")
        username.send_keys(self.user)
        password = self.driver.find_element_by_xpath("//input[@name=\"password\"]")
        password.send_keys(self.password)
        self.driver.find_element_by_xpath("//button[@type=\"submit\"]") \
            .click()
        # Wait to load page
        time.sleep(10)
        # click on turn on button
        self.driver.find_element_by_xpath("//button[contains(text(),'Not Now')]") \
            .click()
        # Wait to load page
        time.sleep(5)
        # click on profile link
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a") \
            .click()
        self.data["folwrinfo"] = self.scrollFollowers()
        self.data["folinginfo"] = self.scrollFollowing()
        self.getPeopleNotFollowingBck()

    def getPeopleNotFollowingBck(self):
        followersName = self.getFollowerName()
        followingName = self.getFolowingName()
        followersLink = self.data["folwrinfo"]["links"]
        followingLink = self.data["folinginfo"]["links"]
        notFollowingBack = [people for people in followingName
                            if people not in followersName]
        self.profilelinks = [link for link in followingLink
                             if link not in followersLink]
        print("\t\tPeople who are not following me back !")
        table = pd.DataFrame({"Num": "", "Names": notFollowingBack,
                              "Profile Links": self.profilelinks})
        print(table)

    # return the lists of folllowers
    def scrollFollowers(self):
        follower = self.scroll("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a")
        return follower

    # return the lists of following
    def scrollFollowing(self):
        following = self.scroll("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        return following

    def getFollowerName(self):
        followersName = self.data["folwrinfo"]["name"]
        return followersName

    def getFolowingName(self):
        followingName = self.data["folinginfo"]["name"]
        return followingName

    # returns the names list
    def scroll(self, element):
        # Wait to load page
        time.sleep(10)
        # click on follower or following  list
        self.driver.find_element_by_xpath(element) \
            .click()
        time.sleep(5)
        # grab the scroll container
        scrollbar = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        # Get scroll height
        last_height = self.driver.execute_script("return arguments[0].scrollHeight ", scrollbar)
        # scroll the  list of follower or following amd get the names
        while True:
            # Scroll down to bottom
            self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight)", scrollbar);
            # Wait to load page
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return arguments[0].scrollHeight ", scrollbar);
            elements = self.driver.find_elements_by_class_name("FPmhX")
            if new_height == last_height:
                data = {"links": [e.get_attribute("href") for e in elements],
                        "name": [e.text for e in elements]}
                time.sleep(1)
                self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button") \
                    .click()
                break
            last_height = new_height
        return data


bot = Instabot(email, password)
