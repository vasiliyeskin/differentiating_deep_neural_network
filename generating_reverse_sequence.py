from random import choice, randrange
import csv

def sample(file_name, numberOfStrings, min_length=3, max_length=15):
    fields = ['src', 'trg']
    dict_writer = csv.DictWriter(open(file_name,'w'), fieldnames=fields)
    dict_writer.writeheader()
    data = {}

    for i in range(numberOfStrings):
        random_length = randrange(min_length, max_length)  # Pick a random length
        random_char_list = [choice(characters[:-1]) for _ in range(random_length)]  # Pick random chars
        random_string = ' '.join(random_char_list)
        random_revert = ''.join([x for x in random_string[::-1]])

        data['src'] = random_string
        data['trg'] = random_revert
        dict_writer.writerow(data)



# generate data for the revert toy
if __name__ == '__main__':
    characters = list("abcd")
    sample('toy_revert/train.csv', 10000)