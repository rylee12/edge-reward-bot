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


# https://www.reddit.com/r/MicrosoftRewards/comments/6a7m5w/only_50_points_per_day_for_search/
# Microsoft rewards has different levels. Levels determine how many points u earn
# https://random-data-api.com/
# https://rewards.microsoft.com/pointsbreakdown

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


class BingRewardBot():
    _TEST_TIME = 3
    _SHORT_WAIT = 5
    _STANDARD_WAIT = 7
    _LONG_WAIT = 10

    _dashboard_url = "https://rewards.microsoft.com/"
    _search_url = "https://www.bing.com/search?q="
    _dashboard_points_url = "https://rewards.microsoft.com/pointsbreakdown"

    _msedge_path = "C:\Program Files (x86)\msedgedriver.exe"
    _chrome_path = "C:\Program Files (x86)\chromedriver.exe"
    _profile_path = "--user-data-dir=C:\\Users\\ryanl\\AppData\\Local\\Microsoft\\Edge\\User Data"

    # insert credentials as variables specific to object
    def __init__(self):
        self.driver = None
        self.driver_mode = ""
        self.email = ""
        self.password = ""
    
    def __repr__(self):
        pass

    # combine or keep separate?
    # better way of coding between if desktop or mobile
    def _create_driver(self, mode):
        options = self._setup_driver_options(mode)

        if mode == "desktop":
            driver = Edge(executable_path=msedge_path, options=options)
        
        if mode == "mobile":
            driver = webdriver.Chrome(executable_path=msedge_path, options=options)

        return driver

    # create new driver
    # additional arguments for options such as headers and proxy?
    def _setup_driver_options(self, mode):
        options = EdgeOptions()
        options.add_argument(profile_path)
        options.add_argument("--user-data-dir=C:\\Users\\ryanl\\AppData\\Local\\Microsoft\\Edge\\User d")
        options.use_chromium = True

        options.add_argument("start-maximized")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")

        if mode == "mobile":
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        return options

    # microsoft automatically logs you in
    # TODO: detect for profile or not?
    # https://stackoverflow.com/questions/46878621/logging-into-microsoft-account-using-selenium
    def sign_in(self):
        driver = self._create_driver("desktop")
        #driver.get(dashboard_url)
        driver.get("https://login.live.com/login.srf")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.ID, "io116")).send_keys("ryan.lee1319@outlook.com")
        sleep(30)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(By.ID, "io118")).send_keys("password")


    # create driver later or store in object
    def check_points_iframe(self):
        driver = self._create_driver("desktop")
        driver.get("https://www.bing.com/search?q=hi")
        print(driver.current_url)
        button = driver.find_element_by_xpath("//*[@id='id_rh']")
        sleep(5)
        button.click()
        sleep(5)

        iframe = driver.find_element_by_xpath("//*[@id='bepfm']")
        driver.switch_to.frame(iframe)

        # //*[@id='modern-flyout']/div/div[5]/div/div/div[1]
        desktop_points = driver.find_element_by_xpath("//*[@id='modern-flyout']/div/div[5]/div/div[2]/div[1]/div/div")
        print(desktop_points.text)

        edge_browser_points = driver.find_element_by_xpath("//*[@id='modern-flyout']/div/div[5]/div/div[2]/div[2]/div/div")
        print(edge_browser_points.text)

        mobile_points = driver.find_element_by_xpath("//*[@id='modern-flyout']/div/div[5]/div/div[2]/div[3]/div/div")
        print(mobile_points.text)

        driver.switch_to.default_content()

    # //*[@id="userPointsBreakdown"]/div/div[2]/div/div[{i}]
    # class = title-detail
    # points: //*[@id="userPointsBreakdown"]/div/div[2]/div/div[1]/div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]
    # how to get current browser tab position
    # TODO: return boolean or dictionary of search queries and the max points for each query type
    def check_points_dashboard(self):
        driver = self._create_driver("desktop")
        driver.get(self._dashboard_points_url)

        progress = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='userPointsBreakdown']/div/div[2]/div/div[*]")))
        for i in progress:
            title = i.find_element_by_xpath("./div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[1]")
            points = i.find_element_by_xpath("./div/div[2]/mee-rewards-user-points-details/div/div/div/div/p[2]")
            print(title.text)
            if title.text.startswith("PC"):
                print("PC titles")
            print(points.text)

    # block of code for signing into bing rewards program for first time
    def _rewards_sign_in(self, driver):
        sign_in = driver.find_elements_by_id("raf-signin-link-id")
        if len(sign_in) > 0:
            sign_in[0].click()
            sleep(3)
            

    # how to decide list of words to query?
    def desktop_search(self):
        driver = self._create_driver("desktop")

        for item in edge_words:
            driver.get(f"https://www.bing.com/search?q={item}")

        driver.quit()

    def mobile_search(self):
        driver = self._create_driver("mobile")
        
        for item in mobile_words:
            driver.get(f"https://www.bing.com/search?q={item}")
            sleep(0.3)
        
        driver.quit()


    # detect check mark or other?
    # checked icon class: "mee-icon mee-icon-SkypeCircleCheck"
    def daily_tasks(self):
        driver = self._create_driver("desktop")

        driver.get(self._dashboard_url)
        sleep(2)

        self._rewards_sign_in(driver)

        # differentiate between title and task_title
        for task_number in range(1, 4):
            offer = driver.find_element_by_xpath(f"//*[@id='daily-sets']/mee-card-group[1]/div/mee-card[{task_number}]/div/card-content/mee-rewards-daily-set-item-content/div")
            checked = offer.find_element_by_xpath("./a/mee-rewards-points/div/div/span[1]")
            title = offer.find_element_by_xpath("./a/div[2]/h3")

            print(title.text)
            task_title = title.text.lower().strip()

            # Check if it does not have checkmark since some could have hourglass icon
            # //*[@id="daily-sets"]/mee-card-group[1]/div/mee-card[2]/div
            if checked.get_attribute("class") == "mee-icon mee-icon-AddMedium" or checked.get_attribute("class") == "mee-icon mee-icon-HourGlass":
                self._determine_task(driver, offer, task_title)

        sleep(5)

    # indiv card xpath: //*[@id="more-activities"]/div/mee-card[1]/div/card-content/mee-rewards-more-activities-card-item/div
    # TODO: count number of cards using find elements by (class, xpath?)
    # use * for number?
    def more_activities(self):
        driver = self._create_driver("desktop")

        driver.get(self._dashboard_url)
        sleep(2)

        self._rewards_sign_in(driver)

        more_activties = driver.find_element_by_xpath("//*[@id='more-activities']/div")
        cards = more_activties.find_elements_by_xpath("./mee-card")

        # loop through task cards and determine if there are points to earn
        for i in range(1, len(cards) + 1):
            offer = driver.find_element_by_xpath(f"//*[@id='more-activities']/div/mee-card[{i}]/div/card-content/mee-rewards-more-activities-card-item/div")
            title = offer.find_element_by_xpath("./a/div[2]/h3")

            checked = offer.find_elements_by_xpath("./a/mee-rewards-points/div/div/span[1]")

            # if there is no check or plus symbol, there are no points to earn from that activity card
            if len(checked) > 0:
                checked = checked[0]
            else:
                continue

            task_title = title.text.lower().strip()

            if checked.get_attribute("class") == "mee-icon mee-icon-AddMedium" or checked.get_attribute("class") == "mee-icon mee-icon-HourGlass":
                self._determine_task(driver, offer, task_title)
        
        sleep(5)

    def _determine_task(self, driver, offer, title):
        link = offer.find_element_by_xpath("./a/div[3]/span")
        link.click()
        driver.switch_to.window(driver.window_handles[-1])

        if title == "this or that?":
            print("tot")
            self._solve_this_or_that(driver)
        elif title == "a, b, or c?":
            print("abc")
            self._page_panel_quiz(driver)
        elif title == "supersonic quiz":
            print("sonic fast")
            self._multiple_answers_quiz(driver)
        elif title == "lightspeed quiz":
            print("light speed")
            self._solve_light_speed(driver)
        elif title == "test your smarts":
            print("smart test")
            self._page_panel_quiz(driver)
        elif title == "show what you know":
            print("show know")
            self._page_panel_quiz(driver)
        elif title == "daily poll" or title == "hot takes":
            print("poll")
            self._solve_polls(driver)
        elif title == "true or false":
            print("true or false")
            self._multiple_choices_quiz(driver)
        elif title == "word for word":
            print("words")
            self._multiple_choices_quiz(driver)
        elif title == "who said it?":
            print("say it")
            self._multiple_choices_quiz(driver)
        else:
            print("general task")
            sleep(self._SHORT_WAIT)
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    # TODO: sleep needed?
    def _start_quiz(self, driver):
        try:
            start_button = WebDriverWait(driver, self._LONG_WAIT).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))

            sleep(self._SHORT_WAIT)
            start_button.click()
        except:
            # selenium.common.exceptions.TimeoutException i.e. timeout exception
            print("starting button not present")

    # solve this or that task
    def _solve_this_or_that(self, driver):
        self._start_quiz(driver)

        # wait for btoptions to load?
        while True:
            progress = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "bt_Quefooter"))).text
            current, max = map(int, progress.split(" of "))

            number = random.randint(0, 1)
            driver.find_element_by_id(f"rqAnswerOption{number}").click()
            sleep(self._SHORT_WAIT)

            if current == max:
                header_message = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "headerMessage_Refresh")))

                # get points from rqPoints element or from header message element
                # TODO: why do we want points?
                try:
                    print(header_message.text)
                    points = driver.find_element_by_class_name("rqECredits").text
                    limit = driver.find_element_by_class_name("rqMCredits").text
                    print(f"points = {points}, limit = {limit}")
                except:
                    print("failure in solve this or that quiz")

                break

    # solve quizzes that are on page panel instead of overlay
    # TODO: detect earned message at end of quiz
    # instead of earned message, just detect for any "ending" message
    def _page_panel_quiz(self, driver):
        # wait for presence of questions
        progress = driver.find_element_by_xpath(f"//*[@id='QuestionPane0']/div[2]").text
        progress = re.sub('[()]', '', progress)
        current, max = map(int, progress.split(" of "))

        for i in range(0, max):
            number = random.randint(1, 3)
            option = driver.find_element_by_xpath(f"//*[@id='QuestionPane{i}']/div[1]/div[2]/a[{number}]/div/div/div/span[1]/span")
            option.click()

            # webdriverwait vs find_element
            next = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/main/ol/li[1]/div/div[2]/div[1]/div[1]/div[2]/div[6]/a/div/span/input")))
            next.click()
        
        # is this needed?
        sleep(self._SHORT_WAIT)

        header_message = driver.find_element_by_xpath("//*[@id='ListOfSummaryPanes']")
        print(header_message.text)

    # solve the light speed quiz
    def _solve_light_speed(self, driver):
        self._start_quiz(driver)
        max = self._get_total_circles(driver)

        while True:
            progress = self._get_current_progress(driver)    
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
            sleep(self._SHORT_WAIT)

    # solve overlay quizzes that require user to select multiple answers (up to 5)
    def _multiple_answers_quiz(self, driver):
        self._start_quiz(driver)

        progress_length = self._get_total_circles(driver)

        while True:
            if self._get_current_progress(driver) == progress_length:
                header_message = driver.find_elements_by_class_name("headerMessage_Refresh")
                if len(header_message) > 0:
                    print("quiz is done")
                    break

            answer_index = 0

            try:
                while True:
                    #answers = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqAnswerOption')]")
                    #header_message = driver.find_elements_by_class_name("headerMessage_Refresh")
                    progress = driver.find_element_by_class_name("btCorOps")
                    print(progress.text)
                    current, goal = map(int, progress.text.split("/"))

                    if current == goal:
                        print("fulfilled prophecy")
                        break

                    print(f"prophecy is at: {current}")
                    answer = driver.find_element_by_id(f"rqAnswerOption{answer_index}")
                    if answer.get_attribute("iscorrectoption") == "True":
                        answer.click()
                        sleep(1)

                    answer_index += 1
            except:
                print("exception occurred")
                print(f"current = {current}, goal = {goal}")
            
            sleep(self._SHORT_WAIT)

    # find number of circles in overlay quiz (usually 3)
    # change name to quiz length or max number of questions?
    def _get_total_circles(self, driver):
        circles = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqQuestionState')]")
        return len(circles)

    # get progress of quiz based on number of filled circles
    def _get_current_progress(self, driver):
        circles = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqQuestionState')]")
        current_progress = 0

        # indicate which question user is currently on. Subtract by 1 to find out how many completed
        if len(circles) > 0:
            for circle in circles:
                if circle.get_attribute("class") == "filledCircle":
                    current_progress += 1
        
        return current_progress

    # solve overlay quizzes where user selects one out of multiple choices. Up to 4 questions and 4 choices
    def _multiple_choices_quiz(self, driver):
        start = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "rqStartQuiz")))
        sleep(self._SHORT_WAIT)
        start.click()

        # if multiple choices have more than 2 choices
        choices = driver.find_elements_by_xpath("//*[starts-with(@id, 'rqAnswerOption')]")

        try:
            for number in range(0, len(choices)):
                question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, f"rqAnswerOption{number}")))  
                question.click()

                sleep(self._SHORT_WAIT)
                print(number)

                # check if header_message exists. If it doesn't, then loop again
                header_message = driver.find_elements_by_class_name("headerMessage_Refresh")
                if len(header_message) > 0:
                    # TODO: detect the header message
                    print(header_message)
                    print("anything in header message?")
                    print(header_message[0].text)
                    break
        except:
            print("Error happened")

    # solve daily polls. Two choices to pick
    # check for checkmark instead? maybe percentage of votes?
    def _solve_polls(self, driver):
        number = random.randint(0, 1)
        sleep(self._SHORT_WAIT)
        poll = driver.find_element_by_id(f"btoption{number}")
        poll.click()

        sleep(self._SHORT_WAIT)
        msg = driver.find_element_by_class_name("bt_headerMessage")

        if "earned" in msg.text:
            print("earned in poll")

    # function to load class object with necessary info to do job i.e. driver, sign-in, etc.
    def load(self):
        pass



# TODO:
# ** Only do searches if there are points to earn
# 1. Quizzes and daily tasks
# 2. Complete multiple_answers() function for supersonic quiz task
# 4. Move all common functions such as starting quiz and identifying tasks to other functions
# 5. Use enums
# 6. Transition to random json for searches
# 7. Monthly task cards
# 8. Determine which overlay tasks are not resetted i.e. can be started in-progress (this or that, supersonic quiz)
# 8. Extra: function to download drivers
# can I use same queries for both mobile and pc?
# Automate signing-up into microsoft account (optional)

# NEW TODO problem list:
# 1. Not all searches registering properly -> experiment with sleep times
# 2. Sign-in or not depends on edge settings, need to account for all of it
# 3. multiple answers quiz (supersonic quiz) fails if you start at middle of quiz i.e. 2nd or 3rd question and no start buttons to click
# EXTENSION: experiment with all overlay quizzes restarting
# 4. make it so the functions attempt to re-try and they fail 
#   - solutions: timer? attempt counter?
if __name__=="__main__":
    object1 = BingRewardBot()
    #object1.desktop_search()
    #object1.mobile_search()
    #object1.daily_tasks()
    #object1.more_activities()

    #object1.sign_in()
    object1.check_points_dashboard()
    #object1.check_points_iframe()
