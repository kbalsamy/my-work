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


def get_values(driver, url, uname, pword, month, year, activatedb=None, search=None):

    browser = driver.get(url)
    login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
    login.send_keys(uname)
    password = driver.find_element_by_id("mat-input-1")
    password.send_keys(pword)
    submit = driver.find_element_by_css_selector(".mat-raised-button").click()
    reading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-list-item:nth-child(5) span:nth-child(1)")))
    reading.click()
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

    results = driver.page_source
    b1 = driver.find_element_by_xpath("//*[@id='mat-input-22']").text
    print(b1)

    logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
    logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                             ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
    logout.click()
    driver.quit()
    return results


# scrape('pppp', 'January', 2019, uname='079204720585')

def extract_values(file):
    file = open(file, 'r')
    soup = BS(file, "html.parser")
    table = soup.find_all(class_="datatable-body-cell-label")
    print(table)


html = scrape('pppp', 'January', 2019, uname='079204720584')
result = extract_values('page.html')
