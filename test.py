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
from constants import url
import time


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


def plot_values(results):
    if results:
        getStatement = results.get('generationStatementCharges')
        pprint.pprint(getStatement)
    else:
        print('readings are not found')


def main(url, username, pword):

    options = Options()
    options.headless = False
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
        results = fetch_results(username, '02', '2019', token)
        plot_values(results)
        logout_menu = driver.find_element_by_css_selector(".ml-xs .mat-icon").click()
        logout = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                 ".mat-menu-item:nth-child(5) > .mat-menu-ripple")))
        logout.click()
        driver.quit()
    except (selenium.common.exceptions.WebDriverException, selenium.common.exceptions.TimeoutException) as e:
        driver.quit()
        status = "Error1"
        return status


if __name__ == '__main__':
    
    main(url, '079204720584', 'pppp')
    

