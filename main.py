import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from lxml import etree
import openpyxl

num_of_companies = 12969776
lst = []
INN = {}

# В целом, что-то выдает, данные таблицы и в названии эксель поставлен ИНН.
# Обходит страницы компании, где нет report.

# Что можно сделать:
# - Подчистить эксель-файлы, хотя можно поговорить с Костиным поговорить, в каком формате он хочет видеть информацию
# - Потыкай и все проверь, правильно ли у тебя запускается!
# - Как-то решить и обдумать обход блокировки действий сайта
# - Ну и подчистить код!

# - А так круто, мне нравится твой код, спасибо, молодец!

# Сама функция парсинга report.
def parse_report(url):

    url = url + '/report'
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    page = requests.get(url, headers=headers)
    soup = bs(page.content, 'html.parser')

    tables = pd.read_html(page.content)
    df = tables[0] # берем первую таблицу из списка, то есть то, что нам нужно
    df = df.drop([0]) # убираю повторяющуюся первую строку, для интереса можешь ее убрать и посмотреть
    
    return df



if __name__ == "__main__":

    for i in range(1, 11): #11 для примера
        url = 'https://www.list-org.com/company/' + str(i)
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        page = requests.get(url, headers=headers)
        soup = bs(page.content, "html.parser")

        # временный try/except, чтобы предупреждать, когда сайт видит подозрительную активность
        try:
            info_1 = soup.find('table', {'class': 'tt'})
            table_1 = info_1.find_all('tr')
            name = soup.find('div', {'class': 'c2m'}).find('a').text
        except AttributeError:
            print("Сайт думает, что вы робот, который бессовестно его парсит!")   
            break

        d = dict()
        d['Полное юридическое наименование:']=name
        for tr in table_1:
            k, v = bs(str(tr), 'html.parser').findAll('td')
            d[k.text] = v.text

            # Составляем списочек ИНН.
            # Твой код понятен, и переменные нормально названы!

            if k.text == 'ИНН / КПП:':
                index = v.text.rfind(' / ')
                INN[i] = v.text[:index]

        lst.append(d)

        # try/except - для того, чтобы пропускал компании, у которых нет отчетности
        try:
            report_df = parse_report(url)
            with open(INN[i] + '.xlsx', 'wb') as output:
                writer = pd.ExcelWriter(output, engine='openpyxl', index=False)
                report_df.to_excel(writer)
                writer.save()

            print(report_df)

        except ImportError:
            pass
    
    # Для сверки можешь вывести словарь с ИНН, где ключ - номер компании, а значение - ИНН
    # print(INN)

    df = pd.DataFrame(lst)
    df.to_csv('list-org.csv', index=False)