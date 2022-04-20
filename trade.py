"""

this algorithm automates the trading of BTC/USDT on the cgzg trading website
the excel file contains a simple trading strategy. It begins with the first trade in Sheet2(Side 1) column which
is a fall and bids the respective amount at the "Buy" column. If it's successful it follows a rise in the next line and bids the
respective amount. If it successful it moves on the next. At any point the trade is not successful if begins the trade loop.
The automation runs based on the length of data on the Stage column.

"""


# importing libraries
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from openpyxl import load_workbook
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time

# define driver variables
s = Service("chromedriver.exe")
driver = webdriver.Chrome(service=s)
# url = "https://cgzg.net/trade#BTC/USDT"
# url = "https://www.cgzg.net/trade/simulate"
url = "https://cgzg.net/account/login"
driver.get(url)

# load excel file and define data values
tradeFile = pd.read_excel('trade.xlsx', sheet_name='Sheet2')
tradeFileDf = tradeFile.iloc[0:9, 0:5] # specify trade table strategy
tradeLength = len(tradeFileDf['Stage']) #length of trade

# login credentials
number = '0557187667'
password = '1nnocent'


# this function begins the trade. It enters the login credentails on the trading site, and trades based on the strategy in the excel file. See strategy
# explanation at the beginning of file

def startTrade():
    driver.find_element(By.XPATH, '//*[@id="app"]/article/main/section[2]/div[1]/input').send_keys(number) # number login credentials
    driver.find_element(By.XPATH, '//*[@id="app"]/article/main/section[2]/div[2]/input').send_keys(password) # password login credentials
    driver.find_element(By.XPATH, '//*[@id="app"]/article/main/section[3]/button').click() # login button
    time.sleep(7)
    driver.find_element(By.XPATH, '//*[@id="app"]/article/footer/nav/a[2]').click() # trade button


# begins the loop with the first trade
    i = 0
    while i < tradeLength:

        print(tradeFileDf['Side 1'][i])
        print(tradeFileDf['Buy'][i])

# checks the value of the trade columns and trades based on those values

        if tradeFileDf['Side 1'][i] == 'Rise':
            tradeResult = rise(tradeFile['Buy'][i])
        elif tradeFileDf['Side 1'][i] == 'Fall':
            tradeResult = fall(tradeFile['Buy'][i])


        print (tradeResult)

# if trade is not successful begin the loop, if successful, continue the loop
        if tradeResult != tradeFileDf['Side 1'][i]:
            i = 0;
        else:
            i += 1

# trade a rise
def rise(amount):
    amount = str(amount)
    # driver.implicitly_wait(10)
    time.sleep(6)
    driver.find_element(By.XPATH, '//*[@id="app"]/article[1]/main/section[6]/button[1]').click()  # trade button
    time.sleep(6)
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[4]/section/main/section/section/main/section[1]/header[4]/div/div/input').clear() # amount input clear
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[4]/section/main/section/section/main/section[1]/header[4]/div/div/input').send_keys(
        amount)  # amount input
    time.sleep(15)
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[4]/section/main/section/section/main/section[2]/button[2]').click()  # confirm button
    # driver.implicitly_wait(2)
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[5]/section/footer/button[2]').click()  # confirm transaction button
    driver.find_element(By.XPATH, '//*[@id="app"]/article[4]/section/footer/div').click()  # close trade popup
    remainingTime = driver.find_element(By.XPATH,
                                        '//*[@id="app"]/article[1]/main/section[5]/header[3]/div[3]/span').text  # remaning time text
    remainingTimeSplit = str(remainingTime).split(':')
    remainingTimeInSeconds = int(remainingTimeSplit[0]) * 60 + int(remainingTimeSplit[1])
    print('remaining time in minutes is ' + str(remainingTime))
    print('remaining time in seconds is ' + str(remainingTimeInSeconds))
    # driver.implicitly_wait(remainingTimeInSeconds + 3)
    time.sleep(remainingTimeInSeconds + 3)
    result = driver.find_element(By.XPATH,
                                 '//*[@id="app"]/article[1]/main/section[5]/header[2]/div[2]').text  # settlement result
    return result


# trade a fall
def fall(amount):
    amount = str(amount)
    # driver.implicitly_wait(10)
    time.sleep(6)
    driver.find_element(By.XPATH, '//*[@id="app"]/article[1]/main/section[6]/button[2]').click()  # trade button
    time.sleep(6)
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[4]/section/main/section/section/main/section[1]/header[4]/div/div/input').clear() # amount input clear
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[4]/section/main/section/section/main/section[1]/header[4]/div/div/input').send_keys(
        amount)  # amount input
    time.sleep(15)
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[4]/section/main/section/section/main/section[2]/button[2]').click()  # confirm button
    # driver.implicitly_wait(2)
    time.sleep(2)
    driver.find_element(By.XPATH,
                        '//*[@id="app"]/article[5]/section/footer/button[2]').click()  # confirm transaction button
    driver.find_element(By.XPATH, '//*[@id="app"]/article[4]/section/footer/div').click()  # close trade popup
    remainingTime = driver.find_element(By.XPATH,
                                        '//*[@id="app"]/article[1]/main/section[5]/header[3]/div[3]/span').text  # remaining time text
    remainingTimeSplit = str(remainingTime).split(':')
    remainingTimeInSeconds = int(remainingTimeSplit[0]) * 60 + int(remainingTimeSplit[1])
    print('remaining time in minutes is ' + str(remainingTime))
    print('remaining time in seconds is ' + str(remainingTimeInSeconds))
    # driver.implicitly_wait(remainingTimeInSeconds + 3)
    time.sleep(remainingTimeInSeconds + 3)
    result = driver.find_element(By.XPATH,
                                 '//*[@id="app"]/article[1]/main/section[5]/header[2]/div[2]').text  # settlement result
    return result

startTrade()


# updateBalance
def updateBalance(num):
    tradeBook = load_workbook('trade.xlsx')
    tradeBookSheet = tradeBook['Sheet2']
    tradeBookSheet['h2'] = num
    tradeBook.save('trade.xlsx')
