from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from time import sleep
# import undetected_chromedriver.v2 as uc
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import numpy as np
import pickle

# import mouse


global driver
global follow_list
global unfollow_list


class CreateDriver:
    global driver
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "localhost:8989")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # open google if successful
    driver.get("http://google.com")


# if not logged into google (better with undetected_chromedriver.v2 used because of ggls security)
def google_login(gmail, google_password):
    driver.get('https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&continue=https%3A%2F%2Fwww\
                .google.com%2F&ec=GAZAmgQ&flowName=GlifWebSignIn&flowEntry=ServiceLogin')
    sleep(1)
    driver.find_element(By.ID, "identifierId").send_keys(gmail)
    driver.find_element(By.CSS_SELECTOR, '#identifierNext > div > button').click()
    sleep(2)
    driver.find_element(By.NAME, "password").send_keys(google_password)
    driver.find_element(By.ID, "passwordNext").click()


# if not logged into google and want to keep it that way (sends alert notification)
def instagram_login(username, password):
    driver.get("https://instagram.com")
    sleep(2.5)
    # Locate the username field
    unform = driver.find_element(By.NAME, "username")
    # Locate the password field
    pwform = driver.find_element(By.NAME, "password")

    ActionChains(driver) \
        .move_to_element(unform).click() \
        .send_keys(username) \
        .move_to_element(pwform).click() \
        .send_keys(password) \
        .perform()

    # Locate login button
    login_button = driver.find_element(By.XPATH, "//div[contains(text(),'Log In')]")
    # Click login button
    login_button.click()
    sleep(3)


def scroll_to_bottom(bottom_element):
    ActionChains(driver) \
        .scroll_to_element(bottom_element) \
        .perform()


def simulate_scrolling(element, xoff, yoff):
    ActionChains(driver) \
        .move_to_element_with_offset(element, xoff, yoff) \
        .click_and_hold(element) \
        .perform()


def row_element_xpath(num=12):
    start = '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/div[' \
            '1]/div/div['
    index = str(num)
    end = ']'
    element = start + index + end
    return element


def row_element_text_xpath(num=0):
    start = '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/div[' \
            '1]/div/div['
    index = str(num)
    end = ']/div[2]/div[1]/div/div/span/a/span/div'

    element = start + index + end
    str(element)
    return driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/\
    div/div/div/div/div[3]/div[1]/div/div[1]/div[2]/div[1]/div/div/span/a/span/div').text


def create_following_list():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    global follow_list
    follow_list = np.array([])
    for link in soup.find_all('a'):
        acc_link = str(link.get('href'))
        acc_link.count('/')
        if acc_link.count('/') == 2:
            follow_list = np.append(follow_list, link.get('href'))

    index = [0, 1, 2]
    follow_list = np.delete(follow_list, index)
    follow_list = np.unique(follow_list)

    filehandler = open("Following.txt", "wb")
    pickle.dump(follow_list, filehandler)
    filehandler.close()


def follow_page(username="/xen_py/"):
    return "https://www.instagram.com" + username + "following/"


def make_unfollow_list():
    global follow_list
    global unfollow_list
    unfollow_list = np.array([])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    file = open('Following.txt', 'rb')
    follow_list = pickle.load(file)
    file.close()

    for user in follow_list:
        driver.get(follow_page(user))
        print('checking ' + "@" + user.replace("/", ""))
        sleep(4)
        """
        if row_element_text_xpath(1) == Actions.username:
            # unfollow_list.append(row_element_text_xpath(1))
            unfollow_list = np.append(unfollow_list, row_element_text_xpath(1))
        else:
            unfollow_list = np.append(unfollow_list, user)
            # unfollow_list.append(user)
        """
        for link in soup.find_all('a'):
            acc_link = str(link.get('href'))
            if Actions.username in acc_link:
                unfollow_list = np.append(unfollow_list, Actions.username)
            else:
                unfollow_list = np.append(unfollow_list, user)

    not_following = unfollow_list != Actions.username
    unfollow_list = unfollow_list[not_following]

    for user in unfollow_list:
        print(user)
    # write file
    filehandler = open("UnfollowList.txt", "wb")
    pickle.dump(unfollow_list, filehandler)
    filehandler.close()




class Actions:

    username = ""

    def __init__(self, username, password):
        Actions.username = username
        self.password = password
        self.following = None
        self.num_following = None

    def loginit(self):

        username = Actions.username

        # assuming already logged into insta
        driver.get("https://www.instagram.com/" + username + "/")
        sleep(2)
        self.num_following = int(driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div\
            /div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span').text.replace(',', ''))
        self.following = [self.num_following]
        driver.get("https://www.instagram.com/" + username + "/following/")
        print(self.num_following)

    def make_lists(self):

        multiples = int(self.num_following / 12)
        print(multiples)
        sleep(1)
        # print(panel.location)
        # print(panel.size)
        # simulate_scrolling(panel, 398, -190)

        for i in range(1, multiples):
            div_index = i * 12
            row = driver.find_element(By.XPATH, row_element_xpath(div_index))
            scroll_to_bottom(row)
            print(str(div_index) + ' followers found out of: ' + str(multiples*12))
            sleep(5.2)

        create_following_list()
        make_unfollow_list()

    @staticmethod
    def unfollow():
        global unfollow_list
        file = open('UnfollowList.txt', 'rb')
        unfollow_list = pickle.load(file)
        file.close()
        print(unfollow_list)
        unfollow_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/\
        section/main/div/header/section/div[3]/div/div[2]/button')
        unfollow_confirmation = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/div/\
        div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]/button[1]')

        for user in range(0, 200):
            driver.get(follow_page(unfollow_list[user]))
            sleep(4)
            unfollow_button.click()
            sleep(1)
            unfollow_confirmation.click()
            sleep(20)

