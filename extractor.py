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


def db_connect():
    con = sqlite3.connect('ReadingsV1onAPP.db')
    return con


def scrape(pword, month, year, servicelist=None, uname=None):
    " webdriver created here"
    options = Options()
    options.headless = True
    binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
    driver = webdriver.Firefox(options=options, firefox_binary=binary)
    if uname:
        results = get_values(driver, url, uname, pword, month, year)
        return results
    else:
        batch = [servicelist[i:i + 15] for i in range(0, len(servicelist), 15)]
    for row in range(len(batch)):
        tab = 0
        for ID in batch[row]:
            driver.execute_script("window.open('about:blank', 'tab{}');".format(tab))
            driver.switch_to.window("tab{}".format(tab))
            get_values(driver, url, ID, pword, month, year, activatedb=True)
            tab += 1
    driver.quit()
    timestr = time.asctime()
    logging.info('{} Batch download is completed'.format(timestr))


def get_values(driver, url, uname, pword, month, year, activatedb=None):
    "Scaping logic "
    try:
        browser = driver.get(url)
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        login.send_keys(uname)
        password = driver.find_element_by_id("mat-input-1")
        password.send_keys(pword)
        submit = driver.find_element_by_css_selector(".mat-raised-button").click()
        try:
            reading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mat-list-item:nth-child(2) span:nth-child(1)")))
            reading.click()
            menu_selector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mat-select-1 .mat-select-arrow"))).click()
            element = driver.find_element_by_css_selector(".ng-trigger-transformPanel")
            actions = ActionChains(driver)
            actions.move_to_element(element).perform()
            select_month = driver.find_element_by_css_selector(month_dict.get(month)).click()

            enter_year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-5")))
            enter_year.clear()
            enter_year.send_keys(year)
            try:
                enter_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".primary > .mat-button-wrapper"))).click()

                fetch_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mr-1 > .mat-button-wrapper"))).click()
                soup = BS(driver.page_source, "lxml")
                html = soup.prettify()
                status = "Successfully extracted the values for {}".format(uname)

                logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
                logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                         ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
                logout.click()
                driver.quit()

                if activatedb:
                    scrape_results = extract_values(uname, html, month, year, status, dbconnect=db_connect())

                else:
                    scrape_results = extract_values(uname, html, month, year, status)
                    return scrape_results

            except selenium.common.exceptions.TimeoutException as e:
                driver.quit()
                status = "Readings are not found for {}.".format(uname)
                if activatedb:
                    scrape_results = extract_values(uname, html, month, year, status, dbconnect=db_connect())
                else:
                    scrape_results = extract_values(uname, None, month, year, status)
                    return scrape_results

        except selenium.common.exceptions.TimeoutException as e:
            driver.quit()
            status = "Time out, please try again or contact admin."

            if activatedb:
                scrape_results = extract_values(uname, None, month, year, status, dbconnect=db_connect())
            else:
                scrape_results = extract_values(uname, None, month, year, status)
                return scrape_results

    except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.TimeoutException) as e:
        driver.quit()
        status = "Check your internet connection"
        if activatedb:

            scrape_results = extract_values(uname, None, month, year, status, dbconnect=db_connect())
        else:
            scrape_results = extract_values(uname, None, month, year, status)
            return scrape_results


def extract_values(uname, html, month, year, status, dbconnect=None):
    "processing the scrapped values"
    final = []
    tablename = month + str(year)
    if html:
        final.append(uname)
        soup = BS(html, "html.parser")
        tab = soup.find("ngx-datatable")
        headers = tab.find_all("span")
        t_list = []
        f_list = []
        for i in headers:
            t_list.append(i.text.strip())
        for i in t_list:
            if i not in f_list and i != "":
                f_list.append(i)
        val = tab.find_all("datatable-body-cell")
        val_list = []
        for i in val:
            val_list.append(i.text.strip())
        results = [val_list[i:i + 9] for i in range(0, len(val_list), 9)]
        imp = [val[4] for val in results]
        exp = [val[8] for val in results]
        dif = [float(exp[i]) - float(imp[i]) for i in range(len(imp))]
        final.append(imp + exp + dif)
        timestr = time.asctime()
        logging.info('{} : Data fetched for {}'.format(timestr, uname))
        if dbconnect:
            cursor = dbconnect.cursor()
            create_table = """CREATE TABLE IF NOT EXISTS {} (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, consumer TEXT, Connection TEXT, ImportUnits REAL, ExportUnits REAL, DifUnits REAL)""".format(tablename)
            cursor.execute(create_table)
            for item in results:
                differnce = float(item[8]) - float(item[4])
                insert_values = """INSERT INTO {} (consumer, Connection, ImportUnits, ExportUnits, DifUnits) VALUES(?, ?, ?, ?, ?)""".format(tablename)
                cursor.execute(insert_values, (uname, item[0], float(item[4]), float(item[8]), differnce))
                logging.info('{}:values updated into database for {}'.format(timestr, uname))
                dbconnect.commit()
        else:
            return final

    else:
        timestr = time.asctime()
        logging.info('{} : {}'.format(timestr, status))
        with open('failed summary.txt', 'a+') as file:
            file.write("{} failed to get values\n".format(uname))
            file.close()
        if not dbconnect:
            return status
