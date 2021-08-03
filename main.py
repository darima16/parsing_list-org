import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

num_of_companies = 12969776
lst = []
for i in range(1, 11): #11 для примера
    url = 'https://www.list-org.com/company/' + str(i)
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, "html.parser")

    info_1 = soup.find('table', {'class': 'tt'})
    table_1 = info_1.find_all('tr')
    name = soup.find('div', {'class': 'c2m'}).find('a').text
    d = dict()
    d['Полное юридическое наименование:']=name
    for tr in table_1:
        k, v = bs(str(tr), 'html.parser').findAll('td')
        d[k.text] = v.text
    lst.append(d)

df = pd.DataFrame(lst)
df.to_csv('list-org.csv', index=False)



