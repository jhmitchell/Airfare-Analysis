from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.common.exceptions import TimeoutException

def get_driver():
    '''
    Configure and return the selenium webdriver
    '''

    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    return webdriver.Chrome(options = chrome_options)

def get_flights(driver, source, target):
    '''
    Find the cheapest roundtrip airfare between the location of departure
    and the destination
    '''

    # Visit google flights
    driver.get('https://www.google.com/travel/flights')
    sleep(5)
    
    # Enter the departure location
    dep = driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[1]/div/div/div[1]/div/div/input")
    #dep = driver.find_element(By.XPATH, "//*[@id='ow49']/div[1]/div/div/input")
    dep.click()
    sleep(1)
    #dep_dd = driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input")
    dep_dd = driver.find_element(By.XPATH, "//*[@id='i15']/div[6]/div[2]/div[2]/div[1]/div/input")
    dep_dd.send_keys(source)
    dep_dd.send_keys(Keys.ENTER)

    # Enter the destination
    dest = driver.find_element(By.XPATH, "//input[@class='II2One j0Ppje zmMKJ LbIaRd' and @placeholder='Where to?']")
    dest.click()
    sleep(1)
    dest_dd = driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input")
    dest_dd.send_keys(target)
    dest_dd.send_keys(Keys.ENTER)

    # Search
    search = driver.find_element(By.XPATH, "//span[text()='Search']")
    search.click()
    sleep(5)

if __name__ == '__main__':
    driver = get_driver()
    get_flights(driver, 'Chicago', 'Harrisburg')