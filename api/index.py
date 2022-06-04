import json
from functools import cmp_to_key
from http.server import BaseHTTPRequestHandler
from bs4 import BeautifulSoup
import requests


def cmp(x, y):
    date1 = x.get("date")
    date2 = y.get("date")
    return date1 < date2


def get_data(name):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73"}
    url = "https://gitee.com/charles-min"
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    less_days = soup.find_all("div", class_="box less")
    little_days = soup.find_all("div", class_="box little")
    some_days = soup.find_all("div", class_="box some")
    much_days = soup.find_all("div", class_="box much")
    days = less_days + little_days + some_days + much_days
    days.sort(key=cmp_to_key(cmp))
    res = []
    for day in days:
        split_str = day.get("data-content")
        str_s = split_str.split("：")
        contribute = int(str_s[0][0])
        date = str_s[1]
        item = {"date": date, "count": contribute}
        res.append(item)
    return res


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        user = path.split('?')[1]
        data = get_data(user)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
        return
