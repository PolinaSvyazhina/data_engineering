import re

file_name = 'text_1_var_5.txt'
with open(file_name) as file:
    line = file.readlines()

line = ' '.join(line)


def replace_punctuation_marks(text):
    new_line = re.sub(r'\W', ' ', text)
    return re.sub(' +', " ", new_line)


def cut_line_by_separator(text):
    word_sts = dict()
    words_str = text.split()
    for word in words_str:
        if word in word_sts:
            word_sts[word] += 1
        else:
            word_sts[word] = 1
    return word_sts


words = replace_punctuation_marks(line).lower()
words_dict = cut_line_by_separator(words)
result_dict = dict(sorted(words_dict.items(), reverse=True, key=lambda x: x[1]))

with open('r_text_1_var_5.txt', 'w') as result:
    for key, value in result_dict.items():
        result.write(key + ":" + str(value) + "\n")
