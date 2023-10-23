file_name = "text_2_var_5.txt"
with open(file_name) as file:
    lines = file.readlines()

average = list()
print(lines)
for line in lines:
    element_list = line.split("/")
    count_element = 0
    sum_element = 0

    for item in element_list:
        count_element += 1
        sum_element += int(item)

    average.append(sum_element / count_element)

with open('r_text_2_var_5.txt', 'w') as result:
    for value in average:
        result.write(str(value) + "\n")
