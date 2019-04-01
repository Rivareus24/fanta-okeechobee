import re

from bs4 import BeautifulSoup

"""
url = 'https://www.costa.co.uk/locations/store-locator/map/#latitude=51.5073509&longitude=-0.1277583'
request = urllib.request.Request(url)

try:
    response = urllib.request.urlopen(request)
except ConnectionError:
    print("something wrong")

htmlBytes = response.read()

htmlStr = htmlBytes.decode("utf8")
"""

f = open("data.txt", "r")
htmlStr = f.read()

soup = BeautifulSoup(htmlStr, 'html.parser')

prettify = soup.prettify()

lines = 413

h1s = soup.find_all('h1')[:lines]
h2s = soup.find_all('h2')[:lines]
spans = soup.find_all('span')[:lines]

result = [f"{h1.get_text()}|{h2.get_text()}|{span.get_text()}\n"
          for h1, h2, span in zip(h1s, h2s, spans)]

with open('result.txt', 'a') as out:
    for r in result:
        re_sub = re.sub(' +', ' ', r)
        re_sub = re.sub('\n', '', re_sub)
        out.write(re_sub + '\n')
