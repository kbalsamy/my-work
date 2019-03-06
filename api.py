from selenium import webdriver
import selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.auth import HTTPBasicAuth
import pprint
from constants import *
import time
import logging


def fetch_results(c, m, y, token):
    Requesturl = "http://htoa.tnebnet.org/oa-service//api/gs/generationstatements?dummy=1&edc-id=472&service-number={}&statement-month={}&statement-year={}".format(c, m, y)
    ref = ""
    token = token
    headers = {'Host': 'htoa.tnebnet.org',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
               'Accept': 'application/json, text/plain, */*',
               'Accept-Language': 'en-US,en;q=0.5',
               'Authorization': token,
               'Referer': ref,
               'Content-Type': 'application/json',
               'Connection': 'keep-alive',
               'Cache-Control': 'max-age=0', }
    with requests.Session() as s:
        res = s.get(Requesturl, headers=headers)
        results = res.json()
        try:
            ID = results[0].get('id')
            url = "http://htoa.tnebnet.org/oa-service//api/gs/generationstatement/{}".format(ID)
            finalres = s.get(url, headers=headers)
            finalval = finalres.json()
            return finalval
        except:
            return None


def arrange_results(consumer, readings, charges):

    im = []
    exp = []
    dif = []
    ban = []
    for i in range(len(readings)):
        im.append(readings[i].get('impUnits'))
        exp.append(readings[i].get('expUnits'))
        dif.append(float(exp[i]) - float(im[i]))
        ban.append(readings[i].get('bankedBalance'))
    final = [im + exp + dif + ban]
    final.insert(0, consumer)
    chrgs = []
    for i in range(len(charges)):
        row = [charges[i].get('chargeCode'), charges[i].get('chargeDesc'), charges[i].get('totalCharges')]
        chrgs.append(row)
    final.append(chrgs)
    return final


def plot_values(results):

    if results:
        consumer = results.get('dispCompanyServiceNumber')
        getReading = results.get('generationStatementSlots')
        getCharges = results.get('generationStatementCharges')
        return arrange_results(consumer, getReading, getCharges)

    else:
        timestr = time.asctime()
        logging.info('{} :values for {} are not found'.format(timestr, consumer))
        return 'readings are not found'


def fetch(url, username, pword, month, year):

    options = Options()
    options.headless = True
    binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
    driver = webdriver.Firefox(options=options, firefox_binary=binary)
    driver.get(url)
    try:
        login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "mat-input-0")))
        login.send_keys(username)
        password = driver.find_element_by_id("mat-input-1")
        password.send_keys(pword)
        submit = driver.find_element_by_css_selector(".mat-raised-button").click()
        # ID = driver.execute_script("return sessionStorage.getItem('generationStatementId ');")
        token = driver.execute_script("return sessionStorage.getItem('token');")
        results = fetch_results(username, month_selector.get(month), str(year), token)
        logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                 ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
        logout.click()
        driver.quit()
        return results

    except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.TimeoutException) as e:
        driver.quit()
        status = "Error1"
        logging.info('check your internet connction or contact admin')
        return None


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
        charges_valinject = ", ".join('?' * 3)
        charges_results.insert(0, results[0])
        try:
            cursor.execute(insert_values1, row)
            for chaque in charges_results[1:]:
                create_table2 = "INSERT INTO {} VALUES('{}',{})".format(tablename2, consumer, charges_valinject)
                cursor.execute(create_table2, chaque)
            dbcon.commit()
            timestr = time.asctime()
            logging.info('{} :values for {}are stored in database'.format(timestr, consumer))
            return None

        except sqlite3.IntegrityError as e:
            print('already exits')
            timestr = time.asctime()
            logging.info('{} : values for {} already exists'.format(timestr, consumer))
            return "Error4"

    else:
        timestr = time.asctime()
        logging.info('{} :values for {} not found'.format(timestr, consumer))
        return " No results found"


def main(url, pword, mnth, yr, uname=None, serlist=None):

    if uname:
        results = fetch(url, uname, pword, mnth, yr)
        return plot_values(results)
    else:
        tablename1 = mnth + str(yr)
        tablename2 = 'charges' + mnth[0:2] + str(yr)
        db_con = db_connect()
        for s in serlist:
            val = fetch(url, s, pword, mnth, yr)
            result = plot_values(val)
            status = write_to_db(result, db_con, tablename1, tablename2)
        return status
