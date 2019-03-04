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
import itertools
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Appscraper():

    def __init__(self, url, serviceName, servicePass, serviceMonth, serviceYear):
        self.url = url
        self.serviceName = serviceName
        self.servicePass = servicePass
        self.serviceMonth = serviceMonth
        self.serviceYear = serviceYear
        self.meterReadings = []
        self.reading_Charges = []
        self.bankingUnits = []

    def driver(self, noShow=True):
        d = DesiredCapabilities.FIREFOX
        d['loggingPrefs'] = {'browser': 'ALL'}
        options = Options()
        options.headless = noShow
        binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
        driver = webdriver.Firefox(options=options, firefox_binary=binary, capabilities=d)
        return driver

    def scrape(self, driver, page=None):

        driver.get(self.url)
        try:
            login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
            login.send_keys(self.serviceName)
            password = driver.find_element_by_id("mat-input-1")
            password.send_keys(self.servicePass)
            submit = driver.find_element_by_css_selector(".mat-raised-button").click()
            reading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, sections.get(page))))
            reading.click()
            try:
                menu_selector = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#mat-select-1 .mat-select-arrow"))).click()
                element = driver.find_element_by_css_selector(".ng-trigger-transformPanel")
                actions = ActionChains(driver)
                actions.move_to_element(element).perform()
                select_month = driver.find_element_by_css_selector(month_dict.get(self.serviceMonth)).click()
                if page == 'reading':
                    enter_year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-5")))
                    enter_year.clear()
                    enter_year.send_keys(self.serviceYear)
                else:
                    enter_year = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-4")))
                    enter_year.clear()
                    enter_year.send_keys(self.serviceYear)
                try:
                    enter_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".primary > .mat-button-wrapper"))).click()
                    fetch_results = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mr-1 > .mat-button-wrapper"))).click()
                    results = driver.page_source
                    for element in banking:
                        javaScript = "return document.getElementById('{}').value;".format(element)
                        self.bankingUnits.append(driver.execute_script(javaScript))
                    logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
                    logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                             ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
                    logout.click()
                    driver.quit()
                    return results

                except selenium.common.exceptions.TimeoutException as e:
                    driver.quit()
                    status = "Error3"
                    return status

            except selenium.common.exceptions.TimeoutException as e:
                driver.quit()
                status = "Error2"
                return status

        except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.TimeoutException) as e:
            driver.quit()
            status = "Error1"
            return status

    def get_values(self, html, parse=None):

        if html and parse == 'reading':
            self.meterReadings.append(self.serviceName)
            soup = BS(html, "html.parser")
            table = soup.find("ngx-datatable")
            values = soup.find_all("datatable-body-cell")
            temp1 = []
            for val in values:
                temp1.append(val.text.strip())
            temp2 = [temp1[i:i + 9] for i in range(0, len(temp1), 9)]
            imp = [val[4] for val in temp2]
            exp = [val[8] for val in temp2]
            dif = [float(exp[i]) - float(imp[i]) for i in range(len(imp))]
            self.meterReadings.append(imp + exp + dif)
            return self.meterReadings

        elif html and parse == 'statement':
            self.reading_Charges.append(self.serviceName)
            soup = BS(html, "html.parser")
            imp = soup.find_all(class_="datatable-body-cell-label")
            temp3 = []
            for i in range(len(imp)):
                temp3.append((imp[i].text).strip())
            temp4 = [temp3[i:i + 6] for i in range(0, len(temp3), 6)]
            imp = temp4[3]
            imp.pop(0)
            exp = temp4[7]
            exp.pop(0)
            dif = [float(exp[i]) - float(imp[i]) for i in range(len(imp))]
            charges = temp3[68:]
            temp5 = imp + exp + dif + self.bankingUnits
            self.reading_Charges.append(temp5)
            self.reading_Charges.append(charges)
            return self.reading_Charges

        else:
            return None


def main(url, passwd, month, year, page, uname=None, serlist=None):

    if uname:
        crawler = Appscraper(url, uname, passwd, month, year)
        d = crawler.driver()
        html = crawler.scrape(d, page=page)
        result = crawler.get_values(html, parse=page)
        return result
    else:
        tablename1 = month + str(year)
        tablename2 = 'charges' + month[0:2] + str(year)
        db_con = db_connect()
        for s in serlist:
            crawler = Appscraper(url, s, passwd, month, year)
            d = crawler.driver(noShow=False)
            html = crawler.scrape(d, page=page)
            result = crawler.get_values(html, parse=page)
            status = write_to_db(result, db_con, tablename1, tablename2)
        return status


def write_to_db(results, dbcon, tablename1, tablename2):

    cursor = dbcon.cursor()
    create_table1 = """CREATE TABLE IF NOT EXISTS {} (consumer UNIQUE, ImportC1 TEXT, ImportC2 TEXT,ImportC3 TEXT,ImportC4 TEXT, ImportC5 TEXT,ExportC1 TEXT,ExportC2 TEXT,ExportC3 TEXT,ExportC4 TEXT,ExportC5 TEXT, DifUnitC1 REAL, DifUnitC2 REAL, DifUnitC3 REAL, DifUnitC4 REAL, DifUnitC5 REAL, BankingC1 REAL,BankingC2 REAL,BankingC3 REAL,BankingC4 REAL,BankingC5 REAL )""".format(tablename1)
    cursor.execute(create_table1)
    create_table2 = """CREATE TABLE IF NOT EXISTS {} (consumer TEXT, code TEXT, description TEXT, charges TEXT, FOREIGN KEY (consumer) REFERENCES {}(consumer))""".format(tablename2, tablename1)
    cursor.execute(create_table2)
    if results:
        consumer = results[0]
        row = results[1]
        row.insert(0, results[0])
        row_valinject = ", ".join('?' * len(row))
        insert_values1 = """INSERT INTO {} VALUES({})""".format(tablename1, row_valinject)
        charges_results = results[2]
        charges_row = [charges_results[i:i + 3] for i in range(0, len(charges_results), 3)]
        charges_valinject = ", ".join('?' * 3)
        charges_row.insert(0, results[0])
        try:
            cursor.execute(insert_values1, row)
            for chaque in charges_row[1:]:
                create_table2 = "INSERT INTO {} VALUES('{}',{})".format(tablename2, consumer, charges_valinject)
                cursor.execute(create_table2, chaque)
            dbcon.commit()
            return None

        except sqlite3.IntegrityError as e:
            print('already exits')
            return "Error4"

    else:
        return " No results found"


# main(url, 'pppp', 'January', 2019, 'statement', serlist=sample)
# dbcon = db_connect()
# write_to_db(db_res, dbcon, 'January2019', 'chargesjan2019')
