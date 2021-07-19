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
                        
    def set_up(self):
        pass

    def start(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument(self.profile_path)
        driver = Edge(executable_path=self.msedge_path, options=options)
        driver.get("https://www.bing.com/search")
        sleep(1)
        # 2 solutions, insert query string or go to element
        for item in self.edge_words:
            driver.get(f"https://www.bing.com/search?q={item}")
            sleep(1)

        sleep(10)
        driver.quit()

    # test if mobile works for edge. Doesn't crash, but not sure
    def mobile(self):
        mobile_emulation = {
            "deviceName": "iPhone X"
        }
        options = Options()
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument(self.profile_path)
        driver = webdriver.Chrome(executable_path=self.chrome_path, options=options)
        for item in self.mobile_words:
            driver.get(f"https://www.bing.com/search?q={item}")
            sleep(1)
        
        sleep(10)
        driver.quit()
    
    def quiz(self):
        pass


# utility function for class stuff
def do_stuff():
    pass

if __name__=="__main__":
    browser = EdgeRewardBot()
    browser.mobile()
