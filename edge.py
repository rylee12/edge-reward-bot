from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

# For automating data input
from selenium.webdriver.common.keys import Keys

# For providing custom configurations for Chrome to run
from selenium.webdriver.chrome.options import Options

from time import sleep


class EdgeRewardBot():
    # do set up of words in set up function if convenient
    def __init__(self):
        self.msedge_path = "C:\Program Files (x86)\msedgedriver.exe"
        self.chrome_path = "C:\Program Files (x86)\chromedriver.exe"
        self.profile_path = "--user-data-dir=C:\\Users\\ryanl\\AppData\\Local\\Microsoft\\Edge\\User Data"
        self.edge_words = ["hello", "bye", "munch", "crunch", "crow", "dinner", "ant", "water", "fire", "wine",
                            "fire", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
                            "nineteen", "twenty", "twenty-one", "twenty-two", "twenty-three"]
        self.mobile_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
                            "nineteen", "twenty"]
        self.mobile_emulation = {
            "deviceName": "iPhone X"
        }
                        
    def _setup_options(self, options, type: str):
        options.add_argument(self.profile_path)
        if type == "desktop":
            options.use_chromium = True
        
        if type == "mobile":
            options.add_experimental_option("mobileEmulation", self.mobile_emulation)

    def desktop_search(self):
        options = EdgeOptions()
        self._setup_options(options, "desktop")
        driver = Edge(executable_path=self.msedge_path, options=options)
        # 2 solutions, insert query string or go to element
        for item in self.edge_words:
            driver.get(f"https://www.bing.com/search?q={item}")
            sleep(1)

        sleep(5)
        driver.quit()

    # test if mobile works for edge. Doesn't crash, but not sure
    def mobile_search(self):
        options = Options()
        self._setup_options(options, "mobile")
        driver = webdriver.Chrome(executable_path=self.chrome_path, options=options)
        for item in self.mobile_words:
            driver.get(f"https://www.bing.com/search?q={item}")
            sleep(1)
        
        sleep(5)
        driver.quit()
    
    def quiz(self):
        options = EdgeOptions()
        self._setup_options(options, "desktop")
        driver = Edge(executable_path=self.msedge_path, options=options)
        sleep(2)
        # replace xpath with class name for better readability
        rewards = driver.find_element_by_xpath("/html/body/div[1]/div/fluent-design-system-provider/div[2]/div[1]/div[7]")
        rewards.click()
        sleep(10)


# utility function for class stuff
def do_stuff():
    pass


if __name__=="__main__":
    browser = EdgeRewardBot()
    browser.quiz()
    #browser.desktop_search()
    #browser.mobile_search()
