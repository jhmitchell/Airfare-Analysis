from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import numpy as np
import cv2
import pytesseract
from time import sleep
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.common.exceptions import TimeoutException

def get_driver():
    '''
    Configure and return the selenium webdriver
    '''

    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options = chrome_options)
    driver.implicitly_wait(20)
    return driver

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
    #dep_dd = driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input")
    dep_dd = driver.find_element(By.XPATH, "//*[@id='i15']/div[6]/div[2]/div[2]/div[1]/div/input")
    dep_dd.send_keys(source)
    dep_dd.send_keys(Keys.ENTER)

    # Enter the destination
    dest = driver.find_element(By.XPATH, "//input[@class='II2One j0Ppje zmMKJ LbIaRd' and @placeholder='Where to?']")
    dest.click()
    dest_dd = driver.find_element(By.XPATH, "/html/body/c-wiz[2]/div/div[2]/c-wiz/div[1]/c-wiz/div[2]/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[6]/div[2]/div[2]/div[1]/div/input")
    dest_dd.send_keys(target)
    dest_dd.send_keys(Keys.ENTER)

    # Search
    search = driver.find_element(By.XPATH, "//span[text()='Search']")
    search.click()

    # Select the date grid
    dg = driver.find_element(By.XPATH, "//span[text()='Date grid']")
    dg.click()
    sleep(5)

    # This opens a canvas with a grid of prices
    canvas = driver.find_element(By.XPATH, "//canvas")
    
    # Take a screenshot of the canvas element
    screenshot = canvas.screenshot_as_png
    with open('graph.png', 'wb') as f:
        f.write(screenshot)

    extract_prices('graph.png')

def extract_prices(ss):
    '''
    Extract airfare information from a screenshot of a price grid
    '''

    # Load the screenshot image
    image = cv2.imread(ss)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Otsu's thresholding to binarize the image
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Set the custom configuration for pytesseract
    custom_config = r'--psm 6 --oem 3'  

    # Use Tesseract to extract text from the image
    text = pytesseract.image_to_string(thresh, config=custom_config)

    print(text)


if __name__ == '__main__':
    driver = get_driver()
    get_flights(driver, 'Chicago', 'Harrisburg')