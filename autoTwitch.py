import time, random, datetime
import argparse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from config import username, password, streamerURL



class AutoStream:

    def __init__(self, args):
        self.args = args
        self.options = self.browser_options()
        
        file = open('status.txt', 'r')
        self.status = file.readlines()[0]
        file.close()
        self.status = self.status.split(' ')
        
        print(self.status)
        
        self.browser = webdriver.Chrome(executable_path = 'C:\\Users\josep\.wdm\drivers\chromedriver\win32\88.0.4324.96\chromedriver.exe', options=self.options, )
        
        self.wait = WebDriverWait(self.browser, 30)
        self.browser.maximize_window()
        
    def browser_options(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        options.add_experimental_option('useAutomationExtension',False)
        
        #options.binary_location = "./chromedriver.exe"
        

        #Disable webdriver flags or you will be easily detectable
        options.add_argument("--disable-blink-features=AutomationControlled")
        return options
       
    def login(self):
    
        self.browser.get('https://www.twitch.tv/')
        
        time.sleep(random.uniform(1,5))
        
        self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/nav/div/div[3]/div[3]/div/div[1]/div[1]/button').click()
        
        time.sleep(random.uniform(4,6))
        
        usernameIn = self.browser.find_element_by_xpath('//*[@id="login-username"]')
        usernameIn.click()
        usernameIn.send_keys(username)
        
        passwordIn = self.browser.find_element_by_xpath('//*[@id="password-input"]')
        passwordIn.click()
        passwordIn.send_keys(password)
        
        passwordIn.send_keys(Keys.ENTER)
        
        time.sleep(random.uniform(30,40))
        
    def run(self):
    
        self.login()
        
        personalAlreadyGot = [False] * len(self.status)
        
        for i, b in enumerate(self.status):
            if self.status[i] == 't' or self.status[i] == 'T':
                personalAlreadyGot[i] = True
            else:
                personalAlreadyGot[i] = False
        
        trueCount = 0
        
        for item in personalAlreadyGot:
            if item:
                trueCount += 1
        if trueCount != len(personalAlreadyGot):
            for i in range(0, len(streamerURL)):
                if not personalAlreadyGot[i]:
                    links = streamerURL[i]
                    self.browser.get(links)
                    time.sleep(random.uniform(2,5))
                    
                    noError = True
                    name = links.split(".tv/")
                    startTime = ''
                    
                    isPlaying = True
                    temp = self.browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[1]/a/div/div/div/div[2]/div/div/div/p')
                    if not temp:
                            print(name[1] + " Is not live currently. Moving on")
                            noError = False
                    temp = self.browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/a/span')                
                    if not temp:            
                        print(name[1] + " Is not playing " + self.args.game)
                        noError = False
                    elif temp[0].text.lower() != str(self.args.game):
                        print(name[1] + " Is not playing " + self.args.game )
                        noError = False
                        
                        
                    isPlaying = True
                    
                    
                    if noError:
                        print(name[1] + ' Is Live and playing ' + self.args.game)
                        startTime = datetime.datetime.now()
                    while isPlaying and noError:
                        
                        time.sleep(30)
                        
                        
                        # Randomly refresh the page.
                        if random.randint(0,50) == 45:
                            self.browser.get(streamerURL[i])
                        
                        temp = self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[1]/a/div/div/div/div[2]/div/div/div/p').text
                        if temp.lower() != 'live':
                            print(links + " Is no longer live")
                            isPlaying = False
                        temp = self.browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[2]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/a/span').text.lower()
                        if temp != str(self.args.game):
                            print(links + ' Is no longer playing ' + self.args.game)
                            isPlaying = False
                        nowtime = datetime.datetime.now()
                        timeDelta = nowtime - startTime
                        totalSeconds = timeDelta.totalSeconds()
                        mins = totalSeconds/60
                        if mins > 123:
                            print('We have watched for over two hours. Time to move on. Change ' + i + ' in alreadyGot to True')
                            personalAlreadyGot[i] = True
                            isPlaying = False
                            temp = ''
                            for item in personalAlreadyGot:
                                temp = temp + item + ''
                            file = open('status.txt','w')
                            file.write(temp)
                            file.close()
        else:
            print('All drops have been reported as counted. Breaking.')
                        
                
                
                
parser = argparse.ArgumentParser(description='Linkedin Automatic Job Applications')
parser.add_argument('-g','--game', help='What game should the code check for', required=True,default='')

args = parser.parse_args()

bot = AutoStream(args)
bot.run()
