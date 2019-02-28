from selenium import webdriver
import selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as BS
from constants import *
import logging
import time
import sqlite3


def scrape(pword, month, year, uname=None, servicelist=None):
    " webdriver created here"
    options = Options()
    options.headless = False
    binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
    driver = webdriver.Firefox(options=options, firefox_binary=binary)
    results = get_values(driver, url, uname, pword, month, year)
    return results


def get_values(driver, url, uname, pword, month, year, activatedb=None):

    browser = driver.get(url)
    login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
    login.send_keys(uname)
    password = driver.find_element_by_id("mat-input-1")
    password.send_keys(pword)
    submit = driver.find_element_by_css_selector(".mat-raised-button").click()
    reading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "mat-list-item:nth-child(3) span:nth-child(1)")))
    reading.click()
    # driver.find_element_by_css_selector(".mat-drawer-backdrop").click()
    menu_selector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mat-select-1 .mat-select-arrow"))).click()
    element = driver.find_element_by_css_selector(".ng-trigger-transformPanel")
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    select_month = driver.find_element_by_css_selector(month_dict.get(month)).click()
    enter_year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-4")))
    enter_year.clear()
    enter_year.send_keys(year)
    enter_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".primary > .mat-button-wrapper"))).click()
    fetch_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mr-1 > .mat-button-wrapper"))).click()

    with open('page.txt', 'w') as file:
        file.write(driver.page_source)
        file.close()

    logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
    logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                             ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
    logout.click()
    driver.quit()


# scrape('pppp', 'January', 2019, uname='079204720585')

def extract_values(html):
    soup = BS('page', "html.parser")
    imp = soup.find("datatable-header-cell sortable resizeable")
    print(imp)


extract_values('page.html')
