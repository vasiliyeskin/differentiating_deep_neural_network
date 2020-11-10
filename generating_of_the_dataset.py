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

dict_writer = csv.DictWriter(open("differentiating_expressions.txt",'w'), fieldnames=fields)
dict_writer.writeheader()

data = {}
alp_numbers = alphabet + numbers

len_alphabet = len(alphabet)
len_alp_Numb = len(alp_numbers)
for i in range(len_alphabet):
    data['variable'] = alphabet[i]
    n = random.randint(0, len_alp_Numb - 1)
    n = n - 1 if n == i else n
    data['expression'] = '{0} ^ {{ {1} }}'.format(alphabet[i], alp_numbers[n])
    data['result'] = '{1} {0} ^ {{ {1} - 1 }}'.format(alphabet[i], alp_numbers[n])
    dict_writer.writerow(data)

    # derivation of expression of zero degree
    data['expression'] = '{0} ^ {{ {1} }}'.format(alphabet[i], 0)
    data['result'] = '0'
    dict_writer.writerow(data)


### latex to pdf to png for visualization of the result
print(data['expression'])
line = 'test_rendering/test_rendering.png',\
       "\\frac {{ \partial }} {{ \partial {0} }} {1}  = {2}".format(data['variable'], data['expression'],data['result']), 'test.png', True
utils.latex2png(line)


del dict_writer