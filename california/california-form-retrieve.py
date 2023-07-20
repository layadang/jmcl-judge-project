import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium.webdriver.chrome.options import Options

def driver_setup():
    chrome_options = Options()
    prefs = {"download.default_directory": "/Users/phuongdang/Desktop/jmcl-judge-project/california/forms"}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://form700search.fppc.ca.gov/Search/SearchFilerForms.aspx")

    return driver

def send_search(driver, last, first):

    driver.implicitly_wait(10)

    # find input boxes:
    last_input = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/input')
    first_input = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td/input')

    # enter in search terms:
    last_input.send_keys(last)
    first_input.send_keys(first)

    # click enter button
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[2]/div/div")))
    enter_button.click()

    driver.implicitly_wait(30) # wait for result to load

    # click on row to view
    view_button = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[3]/td[7]/a')
    view_button.click()

    driver.implicitly_wait(40) # wait for results to load

    downloaded_years = []
    focused_years = ["2022", "2021", "2020"] # years this project is focusing on

    # locate results table with pdfs
    for i in range(3):
        print(i)
        form_table = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div/table[3]/tbody/tr/td/table[1]/tbody')
        rows = form_table.find_elements(By.XPATH, "./tr")
        driver.implicitly_wait(30)

        for row in rows[1:]: # skip first title row
            cells = row.find_elements(By.TAG_NAME, "td")
            # i = 1 year index
            year = cells[1].text.strip()

            print("now running " + year)

            if year in downloaded_years:
                print(year + " already downloaded")
                continue

            if (year in focused_years): 
                print("downloading " + year)
                download_pdf(driver, cells)
                downloaded_years.append(year)
                break
            
    return

def download_pdf(driver, cells):
    link = cells[1 + 5].find_element(By.TAG_NAME, 'a') # pdf viewer button
    link.click()
    driver.implicitly_wait(30)

    # Download pdf:
    iframe = driver.find_element(By.CSS_SELECTOR, "#ctl00_GenericPopupSizeable_InnerPopupControl_CIF-1")
    driver.switch_to.frame(iframe)

    download_link = driver.find_element(By.XPATH, "/html/body/form/div[3]/table/tbody/tr[2]/td/div/div[4]/object/font/a[3]").get_attribute('href')
    driver.get(download_link)

    driver.switch_to.default_content()
    time.sleep(3) # to finish the download
    driver.implicitly_wait(10)

    # Close pdf window:
    close_pdf_button = driver.find_element(By.XPATH, "/html/body/form/div[5]/div[1]/div/div[1]/div[1]/a")
    close_pdf_button.click()

    driver.implicitly_wait(10)

def main():
    df = pd.read_csv("/Users/phuongdang/Desktop/jmcl-judge-project/california/judge_names_current.csv")
    last_names = df['last_name'].values
    first_names = df['first_name'].values

    for i in range(5):
        driver = driver_setup() # new driver for each search

        current_button = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td[1]')
        current_button.click()

        print("now running " + last_names[i] + " " + first_names[i])
        send_search(driver, last_names[i], first_names[i])
        driver.close()

# call to main
main()