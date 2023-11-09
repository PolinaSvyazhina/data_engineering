import csv
from bs4 import BeautifulSoup

file_name = "text_5_var_5.csv"
with open(file_name) as file:
    lines = file.readlines()
    html = ''
    for line in lines:
        html += line
soup = BeautifulSoup(html, "html.parser")
rows = soup.find_all('tr')[1:]
items = []
for row in rows:
    element = row.find_all('td')
    item = [
        element[0].text,
        element[1].text,
        element[2].text,
        element[3].text,
        element[4].text,
    ]
    items.append(item)

with open('r_text_5_var_5.csv', 'w', newline='', encoding='utf-8') as result:
    writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in items:
        writer.writerow(i)
