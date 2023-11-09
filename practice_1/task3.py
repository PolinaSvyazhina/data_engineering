import math

file_name = "text_3_var_5.txt"
with open(file_name) as file:
    lines = file.readlines()

matrix = []

for line in lines:
    nums = line.strip().split(',')

    result_list = list()

    for index in range(len(nums)):
        if nums[index] == "NA":
            nums[index] = str((int(nums[index - 1]) + int(nums[index + 1])) / 2)
            if math.sqrt(float(nums[index])) > 55:
                result_list.append(nums[index])
        else:
            if math.sqrt(float(nums[index])) > 55:
                result_list.append(nums[index])
    matrix.append(result_list)

with open("r_text_3_var_5.txt", 'w') as result:
    for items in matrix:
        for index, num in enumerate(items):
            result.write(str(num) + (',' if len(items) != index + 1 else '\n'))
