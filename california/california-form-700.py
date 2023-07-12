import time
import csv
# import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# set up driver
driver = webdriver.Chrome()
driver.get("https://form700search.fppc.ca.gov/Search/SearchFilerForms.aspx")

# test function to save html file
def save_html():
    html = driver.page_source
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(html)

# initialize data columns:
first_name = []
last_name = []
middle_init = []
agency = [] 

# algorithm to get results based on input chars (the first two initials of last name)
def searching(chars):
    time.sleep(1)
    # global has_warning
    lastname_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/input")))
    lastname_input.clear()              # clear input box
    lastname_input.send_keys(chars)     # enter in first two initials

    time.sleep(1)
    # click search button
    enter_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[2]/div/div")))
    enter_button.click()

    # check if warning button pops up
    time.sleep(1)

    # if has_warning:
    #     close_warning()                 # call helper function
    #     has_warning = False
    
    # filter to only judges
    time.sleep(2)
    position_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[2]/td[4]/table/tbody/tr/td/input")))
    position_input.clear()              # clear input box
    position_input.send_keys("judge")   # enter in filter term

    # check if there are any results
    if "No data to display" in driver.page_source:
        print("nothing found")
        return
    
    # check if there are multiple pages of results based on bottom pagination bar
    try:
        time.sleep(2)
        pager = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[4]/td/table/tbody/tr/td/div[1]/div')
        pager_info = pager.find_element(By.XPATH, '//*[@id="ctl00_DefaultContent_gridFilers_DXPagerBottom"]/b[1]').text

        # regex match to find number of pages
        match = re.search("(?<=Page 1 of )\d*(?!\d)", pager_info)
        page_num = int(match.group())

    # if there is only one page of results
    except NoSuchElementException:
        page_num = 0


    print("num pages is " + str(page_num))
    time.sleep(1)
    if page_num == 0:   # if there is no "next page" then only collect first page of data once
        collection()
    else:                # else click the next button page_num times and collect data each time
        i = 0
        while (i < page_num) :
            collection()
            next_button = driver.find_element(By.XPATH, "/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[4]/td/table/tbody/tr/td/div[1]/div/a[last()]")
            next_button.click()
            i += 1

    return

# helper function to collect the result that appears in the form of a table
    # only if there are results
def collection():

    time.sleep(1)

    # find the table
    table_result = driver.find_element(By.XPATH, "/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody")
    rows = table_result.find_elements(By.TAG_NAME, "tr")

    # iterate through table results
    for row in rows[15:]:
        cells = row.find_elements(By.TAG_NAME, "td")
        for i in range(len(cells[:5])):
            if (i == 0):
                # print("last name is " + cells[i].text)
                last_name.append(cells[i].text)
            if (i == 1):
                # print("first name is " + cells[i].text)
                first_name.append(cells[i].text)
            if (i == 2):
                if (cells[i].text == " "):
                    # print("middle initial is None")
                    middle_init.append("None")
                else:
                    middle_init.append(cells[i].text)

            # skip 3rd column (its always judge)
            if (i == 4):
                agency.append(cells[i].text)

# helper function to close warning box when there are 500+ results
def close_warning():
    print("attempting to close warning")
    global has_warning
    close_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[2]/div/div[2]/div/div/table/tbody/tr/td/div/div/span')))
    close_button.click()
    print(has_warning)
    has_warning = False

# helper function to save array data to csv
def append_data(first_name, last_name, middle_init, agency):
    data = zip(last_name, first_name, middle_init, agency)
    file_path = "judge_names_current.csv"

    with open(file_path, 'a') as file:
        writer = csv.writer(file)
        writer.writerows(data)

# main function for the scraping program
def main():
    # global has_warning

    # select button to filter only current position
    current_button = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td[1]')
    current_button.click()

    alpha = ['a', 'b', 'c', 'd', 'e', 
             'f', 'g','h','i','j','k',
             'l','m','n','o','p','q',
             'r','s','t','u','v','w',
             'x','y','z']
    
    # add alpha[x: ] on a-loop where x is letter to start scrapping from
    for a in alpha[23:]:
        for b in alpha:

            # # for running without current filter
            # if (a+b) == "ma":
            #     has_warning = True
            #     print("ma detected")
            # else:
            #     has_warning = False

            print("now running: " + a + b)

            searching(a + b)

            append_data(first_name, last_name, middle_init, agency)
            # Clear the lists after appending data
            first_name.clear()
            last_name.clear()
            middle_init.clear()
            agency.clear()

# call to main
main()
