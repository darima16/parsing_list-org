import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

def parse_info(soup):
    res = pd.DataFrame()
    name = soup.find('div', {'class': 'c2m'}).find('a').text
    info_1 = soup.find('table', {'class': 'tt'})
    director = info_1.find_all('tr')[0].find('a').text
    inn_kpp = info_1.find_all('tr')[1].find_all('td')[1].text
    inn = inn_kpp[:11]
    q  = info_1.find_all('tr')[2].find_all('td')[0].find('i').text
    print(q)
    capital = info_1.find_all('tr')[2].find_all('td')[1].text
    personal = info_1.find_all('tr')[3].find_all('td')[1].text
    num_of_founders = info_1.find_all('tr')[4].find_all('td')[1].text
    date = info_1.find_all('tr')[5].find_all('td')[1].text
    print(date)
    status = info_1.find_all('tr')[6].find_all('td')[1].text

    info_2 = soup.find_all('div', {'class': 'c2m'})[1]
    index = re.findall('\d+', info_2.find_all('p')[0].text)[0]
    address = info_2.find_all('p')[1].find('span').text
    gps = info_2.find_all('p')[2].find('a').text
    registered_office = info_2.find_all('p')[3].find('span').text
    lst_of_telephones = info_2.find_all('p')[4].find_all('a')
    telephones = ''
    for i in lst_of_telephones:
        telephones += i.text + ', '
    telephones = telephones[:-2]

    lst_of_faxs = info_2.find_all('p')[5].find_all('a')
    faxs = ''
    for i in lst_of_faxs:
        faxs += i.text + ', '
    faxs = faxs[:-2]
    res = res.append(pd.DataFrame([[name, director, inn,  capital, personal,
                                    num_of_founders, date, status, index, address, gps, registered_office,
                                    telephones, faxs]],
                                    columns=['name', 'director', 'inn', 'capital', 'personal',
                                           'num_of_founders', 'date', 'status', 'index', 'address', 'gps',
                                           'registered_office',
                                           'telephones', 'faxs']),
                                    ignore_index=True)
    return (res)
num_of_companies = 12969776
for i in range(1, 3): #3 для примера
    url = 'https://www.list-org.com/company/' + str(i)
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, "html.parser")
    res = parse_info(soup)
    if i == 1:
        res.to_csv('list-org.csv', index=False)
    else:
        res.to_csv('list-org.csv', mode='a', header=False, index=False)


\