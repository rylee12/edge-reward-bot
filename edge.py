import re
from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

# For automating data input
from selenium.webdriver.common.keys import Keys

# For providing custom configurations for Chrome to run
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait

from time import sleep
import random

from selenium.webdriver.support.wait import WebDriverWait


dashboard_url = "https://account.microsoft.com/rewards/"
dashboard_url2 = "https://rewards.microsoft.com/"
search_url = "https://www.bing.com/search?q="

msedge_path = "C:\Program Files (x86)\msedgedriver.exe"
chrome_path = "C:\Program Files (x86)\chromedriver.exe"
profile_path = "--user-data-dir=C:\\Users\\ryanl\\AppData\\Local\\Microsoft\\Edge\\User Data"

edge_words = ["hello", "comic", "food", "bye", "munch", "crunch", "crow", "dinner", "ant", "water", "fire", "wine",
                    "fire", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "chicken",
                    "beef", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
                    "nineteen", "twenty", "twenty-one", "twenty-two", "twenty-three"]

mobile_words = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                    "s", "t", "u"]

mobile_emulation = {
    "deviceName": "iPhone X"
}

TEST_TIME = 3
SHORT_WAIT = 5
STANDARD_WAIT = 7
LONG_WAIT = 10

# Daily xpaths
# mee-icon mee-icon-SkypeCircleCheck x-hidden-focus (Check mark for if task is done); 'mee-icon-AddMedium'
# checked icon class: "mee-icon mee-icon-SkypeCircleCheck"
# Separate between dailies and activities

# link
# //*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[3]/div/card-content/mee-rewards-daily-set-item-content/div/a/div[3]/span
# icon
# //*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[3]/div/card-content/mee-rewards-daily-set-item-content/div/a/mee-rewards-points/div/div/span[1]
# title
# //*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[3]/div/card-content/mee-rewards-daily-set-item-content/div/a/div[2]/h3

# Activites
# Group of all activity cards
# Add it all back for updated websites

# Use enums for options
def setup_options(options, type: str):
    options.add_argument(profile_path)
    if type == "desktop":
        options.use_chromium = True
    
    if type == "mobile":
        options.add_experimental_option("mobileEmulation", mobile_emulation)


def desktop_search():
    options = EdgeOptions()
    setup_options(options, "desktop")

    driver = Edge(executable_path=msedge_path, options=options)

    for item in edge_words:
        driver.get(f"https://www.bing.com/search?q={item}")
        sleep(1)

    sleep(3)
    driver.quit()


# test if mobile works for edge. Doesn't crash, but not sure
# alter setup_options()
def mobile_search():
    options = EdgeOptions()
    #self._setup_options(options, "mobile")
    options.use_chromium = True
    options.add_argument(profile_path)
    options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver = webdriver.Chrome(executable_path=msedge_path, options=options)
    
    for item in mobile_words:
        driver.get(f"https://www.bing.com/search?q={item}")
        sleep(1)
    
    sleep(3)
    driver.quit()


# Check if card is quiz or poll. If neither, it is daily select
def daily_tasks():
    options = EdgeOptions()
    setup_options(options, "desktop")
    driver = Edge(executable_path=msedge_path, options=options)

    driver.get(dashboard_url2)
    sleep(1)

    for i in range(3, 4):
        offer = driver.find_element_by_xpath(f"//*[@id='daily-sets']/mee-card-group[1]/div/mee-card[{i}]/div/card-content/mee-rewards-daily-set-item-content/div")
        checked = offer.find_element_by_xpath("./a/mee-rewards-points/div/div/span[1]")
        title = offer.find_element_by_xpath("./a/div[2]/h3")

        print(title.text)
        task_title = title.text.lower().strip()

        # Check if it does not have checkmark since some could have hourglass icon
        # //*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[2]/div
        if checked.get_attribute("class") == "mee-icon mee-icon-AddMedium" or checked.get_attribute("class") == "mee-icon mee-icon-HourGlass":
            determine_task_card(driver, offer, task_title)
        else:
            print("false")

    sleep(5)


def start_quiz(driver):
    start_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz"))) # start button

    sleep(0.5)
    start_button.click()


# change checked to complete?
# check to determine if task done by checking points before and after
# Maybe detect if there is an overlay or not
def determine_task_card(driver, offer, title):
    link = offer.find_element_by_xpath("./a/div[3]/span")
    link.click()
    driver.switch_to.window(driver.window_handles[-1])

    if title == "this or that?":
        print("tot")
        this_or_that(driver)
    elif title == "a, b, or c?":
        print("abc")
        page_quiz(driver)
    elif title == "supersonic quiz":
        print("sonic fast")
        multiple_answers(driver)
    elif title == "lightspeed quiz":
        print("light speed")
    elif title == "test your smarts":
        print("smart test")
        page_quiz(driver)
    elif title == "show what you know":
        print("show know")
    elif title == "daily poll" or title == "hot takes":
        print("poll")
        poll_option(driver)
    elif title == "true or false":
        print("true or false")
    elif title == "word for word":
        print("words")
        multiple_choices(driver)
    elif title == "who said it?":
        print("say it")
        multiple_choices(driver)
    else:
        print("general task")
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])


# //*[@id="QuestionPane0"]/div[1]/div[2]/a[1]/div/div/div/span[1]/span
# //*[@id="QuestionPane0"]/div[1]/div[2]/a[2]/div/div/div/span[1]/span
# //*[@id="QuestionPane0"]/div[1]/div[2]/a[3]/div/div/div/span[1]/span
# Answer circle labels: A, B, and C
# Read how many questions there are i.e. track quiz progress
def page_quiz(driver):
    # wait for presence of questions
    progress = driver.find_element_by_xpath(f"//*[@id='QuestionPane0']/div[2]").text
    progress = re.sub('[()]', '', progress)
    current, max = map(int, progress.split(" of "))
    print(current)
    print(max)

    for i in range(0, max):
        number = random.randint(1, 3)
        #option = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//*[@id='QuestionPane{i}']/div[1]/div[2]/a[{number}]/div/div/div/span[1]/span")))
        option = driver.find_element_by_xpath(f"//*[@id='QuestionPane{i}']/div[1]/div[2]/a[{number}]/div/div/div/span[1]/span")
        option.click()

        next = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/main/ol/li[1]/div/div[2]/div[1]/div[1]/div[2]/div[6]/a/div/span/input")))
        next.click()


# While-loop, detect for the "you earned" message
# System for if no start button?
def this_or_that(driver):
    # wait for overlay to load in
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz"))) # start button

    sleep(SHORT_WAIT)
    element.click()

    # wait for btoptions to load?
    while True:
        progress = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bt_Quefooter"))).text
        print(progress)

        current, max = map(int, progress.split(" of "))
        print(current)
        print(max)

        #points = driver.find_element_by_id("rqPoints").text
        #print(points)

        # randint() or choice()
        number = random.randint(0, 1)
        driver.find_element_by_id(f"rqAnswerOption{number}").click()
        #question = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, f"rqAnswerOption{number}")))
        #question.click()

        #sleep(5)

        if current == max:
            print("end")
            header_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "headerMessage_Refresh")))
            break


def true_or_false(driver):
    pass


def multiple_answers(driver):
    circles = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqQuestionState')]")
    current_progress = 0

    # indicate which question user is currently on. Subtract by 1 to find out how many completed
    if len(circles) > 0:
        for circle in circles:
            if circle.get_attribute("class") == "filledCircle":
                current_progress += 1

    print(current_progress)


# Pick answer. If wrong, choose the right answer
def multiple_choices(driver):
    start = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
    sleep(SHORT_WAIT)
    start.click()

    # if multiple choices have more than 2 choices
    choices = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqAnswerOption')]")
    print(len(choices))

    try:
        for number in range(0, len(choices) - 1):
            #number = random.randint(0, 1)

            question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"rqAnswerOption{number}")))  
            question.click()

            sleep(SHORT_WAIT)

            header_message = driver.find_element_by_class_name("headerMessage_Refresh")
            print(header_message)
            print("anything in header message?")

            if "you earned" in header_message.text.lower():
                print("multiple choices done")
                return True
    
    except:
        print("Error happened")

    


# Option 1: //*[@id="btoption0"]
# Option 2: //*[@id="btoption1"]
def poll_option(driver):
    #driver.switch_to.window(driver.window_handles[-1])
    number = random.randint(0, 1)

    poll = driver.find_element_by_id(f"btoption{number}")

    sleep(SHORT_WAIT)
    poll.click()
    #msg = driver.find_element_by_class_name("bt_headerMessage")



# To do:
# 1. Quizzes and daily tasks
# 2. Wait until element loaded function
# 3. Headless mode
# 4. Functionality to check if we have max points
if __name__=="__main__":
    #desktop_search()
    #mobile_search()
    daily_tasks()
