import pandas as pd
import numpy as np
comon_words = ['از','به','با','در','یا','ما','اگر','و','ولی']
df = pd.read_csv('train_test.csv')
words = {}
hafez_beyt_num = 0
saadi_beyt_num = 0
hafez_word_count = 0
saadi_word_count = 0
def make_dic(data):
    global hafez_beyt_num
    global saadi_beyt_num
    global saadi_word_count
    global hafez_word_count
    for index, row in data.iterrows():
        line = row['text'].split(' ')
        if row['label'] == 'hafez':
            hafez_beyt_num += 1
        else:
            saadi_beyt_num += 1
        for item in line:
            if item in comon_words:
                continue
            if item in words:
                words[item][row['label']] +=1
            else:
                words[item] = {'saadi':0, 'hafez':0}
            if row['label'] == 'hafez':
                hafez_word_count += 1
            else:
                saadi_word_count += 1
    num_of_line = hafez_beyt_num + saadi_beyt_num
    hafez_beyt_num /= num_of_line
    saadi_beyt_num /= num_of_line
def calc_probs():
    global saadi_word_count
    global hafez_word_count
    for key in words:
        if words[key]['hafez'] == 0:
            words[key]['hafez']+=1
        if words[key]['saadi'] == 0:
            words[key]['saadi']+=1
        num = words[key]['saadi'] + words[key]['hafez']
        words[key]['saadi'] /= (saadi_word_count)
        # words[key]['saadi'] *= saadi_count
        words[key]['hafez'] /= (hafez_word_count)
        # words[key]['hafez'] *= hafes_count

def find_poem(data, test_flag):
    true_answer = 0
    hafez_num = 0
    counter = 0
    corrctly_detected_hafez = 0
    detected_hafez = 0
    output = []
    for index, row in data.iterrows():
        words_in_line = row['text'].split(' ')
        hafez_prob = 100000
        saadi_prob = 100000
        for item in words_in_line:
            if item not in words:
                continue
            hafez_prob *= words[item]['hafez']
            saadi_prob *= words[item]['saadi']
        # hafez_prob *= ((saadi_beyt_num/hafez_beyt_num)**(len(list(set(words_in_line) - set(comon_words))) -7))
        hafez_prob *= hafez_word_count
        saadi_prob *= saadi_word_count
        if test_flag and ((hafez_prob > saadi_prob and row['label'] == 'hafez') or (saadi_prob > hafez_prob and row['label'] == 'saadi')):
            true_answer += 1
        elif not test_flag:
            output.append([row['id'], 'hafez' if hafez_prob > saadi_prob else 'saadi'])
        if test_flag:
            if row['label']=='hafez':
                hafez_num += 1
                if hafez_prob > saadi_prob:
                    corrctly_detected_hafez += 1
            if hafez_prob > saadi_prob:
                detected_hafez += 1
        # print(output[-1][1])
        counter += 1
    if test_flag:   
        return true_answer/counter, corrctly_detected_hafez / hafez_num, corrctly_detected_hafez/ detected_hafez
    else:
        return output
# for key in words:
#     print(key, words[key])
make_dic(df)
calc_probs()
# print(find_poem(df[:4000], True))
test = pd.read_csv('evaluate.csv')
result = find_poem(test, False)
test = pd.DataFrame(result, columns  = ['index', 'label'])
test.to_csv('result.csv', sep=',', index=False)