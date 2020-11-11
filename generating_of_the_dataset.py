# generating of the dataset
# The data are writen in the latex notation
import csv
import random
import utils.utils as utils



fields = ['variable', 'expression', 'result']

with open('alphabet.txt', 'r') as file:
    alphabet = [line.strip() for line in file.readlines()]

with open('numbers.txt', 'r') as file:
    numbers = [line.strip() for line in file.readlines()]

dict_template_formulas = csv.DictReader(open('template_formulas.txt', newline=''))

dict_writer = csv.DictWriter(open("differentiating_expressions.txt",'w'), fieldnames=fields)
dict_writer.writeheader()

data = {}
alp_numbers = alphabet + numbers

len_alphabet = len(alphabet)
len_alp_Numb = len(alp_numbers)


# generating of the simple expressions
for row in dict_template_formulas:
    for i in range(len_alphabet):
        data['variable'] = alphabet[i]
        n = random.randint(0, len_alp_Numb - 1)
        n = n - 1 if n == i else n

        data['expression'] = row['template_expression'].format(alphabet[i], alp_numbers[n])
        data['result']     = row['template_result'].format(alphabet[i], alp_numbers[n])
        dict_writer.writerow(data)


# generating of the difficult expressions
for row in csv.DictReader(open('template_formulas.txt', newline='')):
    for i in range(len_alphabet):
        data['variable'] = alphabet[i]
        n = random.randint(0, len_alp_Numb - 1)
        n = n - 1 if n == i else n

        inner_expression = row['template_expression'].format(alphabet[i], alp_numbers[n])
        inner_result     = row['template_result'].format(alphabet[i], alp_numbers[n])

        for rowOuter in csv.DictReader(open('template_formulas.txt', newline='')):
            m = random.randint(0, len_alp_Numb - 1)
            m = m - 1 if m == i else m

            difficult_variable = " ( {0} ) ".format(inner_expression)
            data['expression'] = rowOuter['template_expression'].format(difficult_variable, alp_numbers[m])
            data['result'] = "( {0} )".format(inner_result) + rowOuter['template_result'].format(difficult_variable, alp_numbers[m])

            dict_writer.writerow(data)


del dict_writer

### latex to pdf to png for visualization of the result
print(data['expression'])
line = 'test_rendering/test_rendering.png',\
       "\\frac {{ \partial }} {{ \partial {0} }} {1}  = {2}".format(data['variable'], data['expression'],data['result']), 'test.png', True
utils.latex2png(line)

