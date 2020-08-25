from selenium import webdriver
from time import sleep
from credentials import username, password


def write_file(f, x):
    file = open(f, 'w')
    counter = 0
    for item in x:
        file.write("\n%s" % item)
        counter = counter + 1
    file.close()


class InstaBot:

    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com/")
        sleep(2)

        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(6)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    def get_unfollowers(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(3)

        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        print("Getting Following")
        following = self._get_names()
        write_file('following_list.txt', following)

        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        print("Getting Followers")
        followers = self._get_names()
        write_file('followers_list.txt', followers)

        not_following_back = [user for user in following if user not in followers]

        print("Unfollowers :")
        print(not_following_back)
        write_file('unfollowers.txt', not_following_back)

    def _get_names(self):
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[1]/div[2]")
        prev_height, height = 0, 1
        print("Check 1")
        while prev_height != height:
            prev_height = height
            sleep(1)
            height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        print("Check 2")
        links = scroll_box.find_elements_by_tag_name('a')
        print("Check 3")
        names = [name.text for name in links if name.text != '']
        print("Check 4")
        print("Task Complete!")
        self.driver.refresh()
        sleep(3)
        # self.driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[1]/div[1]/div[3]/button").click()
        return names


my_bot = InstaBot(username, password)
try:
    my_bot.get_unfollowers()
    my_bot.driver.close()
except:
    my_bot.driver.close()
