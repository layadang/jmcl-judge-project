import time
import csv
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome()
driver.get("https://form700search.fppc.ca.gov/Search/SearchFilerForms.aspx")

df = pd.read_csv("judge_names_current.csv")
last_names = df['last_name'].values
first_names = df['first_name'].values



def send_search(last, first):
    last_input = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/table/tbody/tr/td/input')
    first_input = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/table/tbody/tr/td/input')

    last_input.send_keys(last)
    first_input.send_keys(first)

    view_button = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[4]/td/table/tbody/tr/td/table[1]/tbody/tr[3]/td[7]/a')
    view_button.click()

    return

def main():
    current_button = driver.find_element(By.XPATH, '/html/body/form/table[1]/tbody/tr/td/table/tbody/tr[4]/td/div/div/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/table/tbody/tr/td[1]')
    current_button.click()

    # for i in range(len(last_names)):
    #     print( last_names[i] + " " + first_names[i])

    send_search(last_names[0], first_names[0])