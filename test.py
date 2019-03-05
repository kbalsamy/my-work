import requests
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import pprint

url = "http://htoa.tnebnet.org/oa/login/login"
getmenu = 'http://htoa.tnebnet.org/oa-report-service/report/org-summaries'

t = 'http://htoa.tnebnet.org/oa/vendor.efd5e292213288728fed.bundle.js'


headers = {'Host': 'htoa.tnebnet.org',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0',
           'Accept': 'application/json, text/plain, */*',
           'Accept-Language': 'en-US,en;q=0.5',
           'Referer': 'http: // htoa.tnebnet.org / oa / gs / gs - list',
           'Authorization': "",
           'Content-Type': 'application/json',
           'Connection': 'keep-alive',
           'Cache-Control': 'max-age=0', }


with requests.Session() as s:

    r = s.get(getmenu, headers=headers)
    c = r.text
    pprint.pprint(c)
    # r2 = s.get(t)
    # pprint.pprint(r2.text)
