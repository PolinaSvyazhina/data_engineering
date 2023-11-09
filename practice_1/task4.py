import csv

average_income = 0
items = list()

file_name = "text_4_var_5.csv"
with open(file_name, newline='\n', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    for row in reader:
        item = {
            'id': int(row[0]),
            'name': row[2] + ' ' + row[1],
            'age': int(row[3]),
            'income': int(row[4][:-1])
        }
        average_income += item['income']
        items.append(item)
        average = average_income / len(items)

result_list = list()
for row in items:
    if row['age'] > (25 + 5 % 10) and row['income'] < average:
        result_list.append(row)

result_list = sorted(result_list, key=lambda x: x['id'])

with open('r_text_4_var_5.csv', 'w', newline='', encoding='utf-8') as result:
    writer = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in result_list:
        writer.writerow(i.values())
