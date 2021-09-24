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
from enum import Enum
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


class SearchModes(Enum):
    DESKTOP = 0
    MOBILE = 1


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

    driver.quit()


# use this function to check points
# *** All 3 points only differ by div number in xpath
def test():
    options = EdgeOptions()
    setup_options(options, "desktop")

    driver = Edge(executable_path=msedge_path, options=options)

    driver.get(f"https://www.bing.com")
    sleep(3)

    # //*[@id='msRewards']//button
    button = driver.find_element_by_xpath("//*[@id='id_rh']")
    button.click()
    sleep(5)

    iframe = driver.find_element_by_xpath("//*[@id='bepfm']")
    driver.switch_to_frame(iframe)

    desktop_points = driver.find_element_by_xpath("//*[@id='modern-flyout']/div/div[5]/div/div[2]/div[1]/div/div")
    print(desktop_points.text)

    edge_browser_points = driver.find_element_by_xpath("//*[@id='modern-flyout']/div/div[5]/div/div[2]/div[2]/div/div")
    print(edge_browser_points.text)

    mobile_points = driver.find_element_by_xpath("//*[@id='modern-flyout']/div/div[5]/div/div[2]/div[3]/div/div")
    print(mobile_points.text)

    driver.switch_to.default_content()

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
    
    driver.quit()


# Check if card is quiz or poll. If neither, it is daily select
def daily_tasks():
    options = EdgeOptions()
    setup_options(options, "desktop")
    driver = Edge(executable_path=msedge_path, options=options)

    driver.get(dashboard_url2)
    sleep(1)

    # block of code for signing into bing rewards program for first time
    """
    sign_in = driver.find_elements_by_id("raf-signin-link-id")
    if len(sign_in) > 0:
        print("sign into stuff")
        sign_in[0].click()
        sleep(2)
    """

    for i in range(1, 4):
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

    sleep(SHORT_WAIT)
    start_button.click()


def determine_type(driver):
    overlay = len(driver.find_elements_by_id("btPollOverlay"))
    print(overlay)
    panel = len(driver.find_elements_by_id("ListOfQuestionAndAnswerPanes"))
    print(panel)



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
        light_speed(driver)
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
        multiple_choices(driver)
    elif title == "word for word":
        print("words")
        multiple_choices(driver)
    elif title == "who said it?":
        print("say it")
        multiple_choices(driver)
    else:
        print("general task")
        sleep(SHORT_WAIT)
    
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

        # /html/body/div[2]/main/ol/li[1]/div/div[2]/div/div[1]/div[2]/div[6]/a/div/span/input (Get score button)
        # /html/body/div[2]/main/ol/li[1]/div/div[2]/div[1]/div[1]/div[2]/div[6]/a/div/span/input (Next question button)
        # "b_focusLabel wk_rewards_promo"
        next = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/main/ol/li[1]/div/div[2]/div[1]/div[1]/div[2]/div[6]/a/div/span/input")))
        next.click()
    
    sleep(SHORT_WAIT)
    score = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/main/ol/li[1]/div/div[2]/div/div[1]/div[2]/div[6]/a/div/span/input")))
    score.click()

    header_message = driver.find_element_by_class_name("b_focusLabel wk_rewards_promo")
    print(header_message.text)
    sleep(120)


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

        # randint() or choice()
        number = random.randint(0, 1)
        driver.find_element_by_id(f"rqAnswerOption{number}").click()
        #question = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, f"rqAnswerOption{number}")))
        #question.click()

        sleep(SHORT_WAIT)

        if current == max:
            print("end")
            header_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "headerMessage_Refresh")))
            print(header_message)
            print("anything in header message?")

            # get points from rqPoints element or from header message element
            try:
                print(header_message.text)
                points = driver.find_element_by_class_name("rqECredits")
                limit = driver.find_element_by_class_name("rqMCredits")
            except:
                print("failure")

            break


def start_overlay_quiz(driver):
    start_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz"))) # start button

    sleep(SHORT_WAIT)
    start_button.click()


def get_current_progress(driver):
    circles = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqQuestionState')]")
    current_progress = 0

    # indicate which question user is currently on. Subtract by 1 to find out how many completed
    if len(circles) > 0:
        for circle in circles:
            if circle.get_attribute("class") == "filledCircle":
                current_progress += 1
    
    return current_progress


def get_progress_length(driver):
    circles = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqQuestionState')]")
    return len(circles)


# track progress and then answer choices. Once all correct choices answered, wait and then check progress again, repeat
# when progress is equal to number of circles, check if header message available. if not, then do questions again and then check again
def multiple_answers(driver):
    element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz"))) # start button

    sleep(SHORT_WAIT)
    element.click()

    circles = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqQuestionState')]")
    current_progress = 0

    # indicate which question user is currently on. Subtract by 1 to find out how many completed
    if len(circles) > 0:
        for circle in circles:
            if circle.get_attribute("class") == "filledCircle":
                current_progress += 1


    progress = driver.find_element_by_class_name("btCorOps")
    print(progress.text)
    current, max = map(int, progress.text.split("/"))

    answers = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqAnswerOption')]")
    #header_message = driver.find_elements_by_class_name("headerMessage_Refresh")
    for answer in answers:
        count = 0
        answer.click()
        sleep(2)    



# Pick answer. If wrong, choose the right answer
def multiple_choices(driver):
    start = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
    sleep(SHORT_WAIT)
    start.click()

    # if multiple choices have more than 2 choices
    choices = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqAnswerOption')]")
    print(len(choices))

    try:
        for number in range(0, len(choices)):
            question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"rqAnswerOption{number}")))  
            question.click()

            sleep(SHORT_WAIT)

            # check if header_message exists. If it doesn't, then loop again
            header_message = driver.find_elements_by_class_name("headerMessage_Refresh")
            if len(header_message) > 0:
                # TODO: detect the header message
                print(header_message)
                print("anything in header message?")
                print(header_message[0].text)
    
    except:
        print("Error happened")


# difference is light speed has more than one question
def light_speed(driver):
    start_overlay_quiz(driver)
    max = get_progress_length(driver)

    while True:
        progress = get_current_progress(driver)    
        if progress == max:
            print("progress done")
            header_message = driver.find_elements_by_class_name("headerMessage_Refresh")
            # if header_message is not there, then it will be an empty list

            if len(header_message) > 0:
                print("congrats, you are done")
                break

        choices = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqAnswerOption')]")
        random_choice = random.randint(0, 3)
        choices[random_choice].click()
        sleep(SHORT_WAIT)


# Option 1: //*[@id="btoption0"]
# Option 2: //*[@id="btoption1"]
def poll_option(driver):
    number = random.randint(0, 1)

    poll = driver.find_element_by_id(f"btoption{number}")

    sleep(SHORT_WAIT)
    poll.click()

    sleep(STANDARD_WAIT)
    msg = driver.find_element_by_class_name("bt_headerMessage")
    print("poll message")
    print(msg)
    print(msg.text)

    if "earned" in msg.text:
        print("earned in poll")



# TODO:
# Only do searches if there are points to earn
# 1. Quizzes and daily tasks
# 2. Complete multiple_answers() function for supersonic quiz task
# 3. Move all functions into a class object
# 4. Move all common functions such as starting quiz and identifying tasks to other functions
# 5. Use enums
# Automate signing-up into microsoft account (optional)
# End-game goal: AWS Lambda?
if __name__=="__main__":
    #desktop_search()
    #mobile_search()
    daily_tasks()
    #test()
