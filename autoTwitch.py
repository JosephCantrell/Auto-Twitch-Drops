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
        
        # THIS PATH NEEDS TO BE CHANGED TO YOUR LOCAL CHROME DRIVER PATH. This has to be in the code to allow for the options. I couldnt get around this
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
        
        time.sleep(random.uniform(0,2))
        
        passwordIn = self.browser.find_element_by_xpath('//*[@id="password-input"]')
        passwordIn.click()
        passwordIn.send_keys(password)
        
        passwordIn.send_keys(Keys.ENTER)
        
        # THIS DELAY IS LONG DUE TO CAPTCHA ON MY END EVERY TIME I USE THE CODE
        time.sleep(random.uniform(40,60))
        
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
        while True:
            if trueCount != len(personalAlreadyGot) or self.args.loop:
                for i in range(0, len(streamerURL)):
                    if not personalAlreadyGot[i] or self.args.loop:
                        links = streamerURL[i]
                        self.browser.get(links)
                        time.sleep(random.uniform(2,5))
                        
                        noError = True
                        name = links.split(".tv/")
                        startTime = ''
                        
                        foundLive = False
                        isPlayingGame = False
                        isPlaying = False
                        
                        time.sleep(5)
                        
                        # Find the "Live" element.
                        foundLive = self.findLiveElement()
                        
                        # Only do the next search if the streamer is Live
                        if foundLive:
                            
                            isPlayingGame = self.findGameElement()


                        if foundLive and isPlayingGame:
                            print(name[1] + ' Is Live and playing ' + self.args.game)
                            startTime = datetime.datetime.now()
                            isPlaying = True
                            while isPlaying:
                                
                                time.sleep(30)
                                
                                
                                # Randomly refresh the page.
                                if random.randint(0,50) == 45:
                                    self.browser.get(streamerURL[i])
                                    time.sleep(10)
                                
                                isPlaying = self.findLiveElement()
                                
                                isPlaying = self.findGameElement()

                                nowtime = datetime.datetime.now()
                                timeDelta = nowtime - startTime
                                totalSeconds = timeDelta.total_seconds()
                                mins = totalSeconds/60
                                if int(args.watchTime) != 0:
                                    if mins > int(args.watchTime) + random.randint(0,3):
                                        print('We have watched for the set time. Time to move on.')
                                        personalAlreadyGot[i] = True
                                        isPlaying = False
                                        trueCount += 1
                                        temp = ''
                                        for item in personalAlreadyGot:
                                            if item:
                                                temp = temp + 't '
                                            else:
                                                temp = temp + 'f '
                                        file = open('status.txt','w')
                                        file.write(temp)
                                        file.close()
                                    else:
                                        print('Still Watching. Its been %d Minute(s)' % mins)
                    else:
                        print('Already Aquired This Drop. Moving On')
                time.sleep(60)
            else:
                print('All drops have been reported as counted. Breaking.')
                break

    def findLiveElement(self):
        temp = self.browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div[1]/a/div/div/div/div[2]/div/div/div/p')
        if not temp:
                print("Could not find the Live Element (Is Offline). Moving on")
                return False
        # Go through the 'Live' elements and search for the text.
        else:
            for items in temp:
                if items.text.lower() == 'live':
                    foundLive = True
                    return True
                return False
    
    def findGameElement(self):
        temp = self.browser.find_elements_by_xpath('//*[@id="root"]/div/div[2]/div/main/div[2]/div[3]/div/div/div[1]/div[1]/div[2]/div/div[1]/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/a/span')   
        # If the streamer is Live and we have found elements in the 
        if not temp:            
            print("Could not find the Game Element (Not Playing Anything). Moving On")
            return False
        # Cycle through the game elements that we found to find the correct element
        else:
            for items in temp:
                # If the current element has the game title that we are looking for, the streamer is playing the correct game
                if items.text.lower() == str(self.args.game.lower()):
                    isPlayingGame = True  
                    return True
                return False

        

parser = argparse.ArgumentParser(description='Linkedin Automatic Job Applications')
parser.add_argument('-g','--game', help='What game should the code check for', required=True,default='')
parser.add_argument('-t','--watchTime', help='How long should the bot watch a streamer for in minutes (Default will watch forever)', required=False,default=0)
parser.add_argument('-l','--loop', help='Loop the code instead of breaking after getting all of the drops', required=False,default=False, action='store_true')

args = parser.parse_args()


bot = AutoStream(args)
bot.run()
