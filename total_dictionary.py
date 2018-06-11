import os
from glob import glob
import re
from optparse import OptionParser
import nltk
from nltk.corpus import wordnet as wn
import collections,re

root = '/Users/wuxinheng/Documents/crawl_dogs/crawl_dogs_700_txt'
# 生成dictionary
def gen_dictionary(file):
    f = open(file,'w')
    dog_name=os.listdir(root)
    for i in dog_name:
        path = os.path.join(root,i)
        for j in os.listdir(path):
            try:
                for line in open(os.path.join(path,j)):
                    f.writelines(line)
                    f.write('\n')
            except Exception as e:
                print(e)
    f.close()

gen_dictionary('dictionary_700.txt')

# 处理forbidden words
in_file = open('forbidden_words.txt', 'r');
forbid_words = set(in_file.read().splitlines());
in_file.close();

# 根据dictionary，生成frequency of words
# freq_dict = {}
# f = open ('dictionary.txt')
# line = f.readline()
# words = line.split(' ')
# for w in words[0:]:
#     if w.isalpha():
#         if w in freq_dict:
#             freq_dict[w]+=1
#         else:
#             freq_dict[w]=1
#
# freq_arr = freq_dict.items()
# #freq_arr.sort(lambda x, y: y[1] - x[1]);
#
# freq_arr= sorted(freq_arr,key = lambda d:d[1] , reverse=True)

# 根据dictionary，生成word_frequency 字典

# 生成word-freq 表
def get_words(file):
    with open (file) as f:
        words_box=[]
        for line in f:
            words_box.extend(line.lower().strip().split())
        new_words_box=[]
        for word in words_box:
            if word.isalpha():
                new_words_box.append(word)
    return collections.Counter(new_words_box)

def get_words_2(file):
    with open (file) as f:
        words_box=[]
        for line in f:
            words_box.extend(line.lower().strip().split())
        new_words_box=[]
        for word in words_box:
            if word.isalpha():
                new_words_box.append(word)
            else:
                new_word=''
                for letter in word:
                    if letter.isalpha():
                        new_word+=letter
                if new_word!='':
                    new_words_box.append(new_word)
    return collections.Counter(new_words_box)

def get_words_3(file):
    with open (file) as f:
        words_box=[]
        for line in f:
            words_box.extend(re.split(r'[;\.\s]*', line))
        new_words_box=[]
        for word in words_box:
            if word.isalpha():
                new_words_box.append(word)
    return collections.Counter(new_words_box)


freq = get_words('dictionary_700.txt')
# freq_2 = get_words_2('dictionary.txt')
# freq_3 = get_words_3('dictionary.txt')
freq_arr = sorted(freq.items(),key = lambda d:d[1] , reverse=True)
# freq_2_arr= sorted(freq_2.items(),key = lambda d:d[1] , reverse=True)
# freq_3_arr= sorted(freq_3.items(),key = lambda d:d[1] , reverse=True)


# nltk.download('averaged_perceptron_tagger')

# 生成word_freq_list （NN JJ VB ）
def gen_freq_words(freq_arr,file):
    outfile = open(file, 'w');
    icount = 0;
    for item in freq_arr:
        if len(item[0]) > 2 and not item[0] in forbid_words:
            pos_tag = nltk.pos_tag([item[0]])[0][1];
            if pos_tag in ['NN', 'JJ', 'VB']:
                print(item[0]);
                outfile.write(item[0] + ' ' + str(item[1]) + '\n');
                icount += 1;
                if icount >= 2000:
                    break;
    outfile.close()

gen_freq_words(freq_arr,'word_freq_700.txt')
# 前300个高频词
def gen_word_dict(dim,file):
    word_dict = {}
    in_file = open(file, 'r')
    for (line_num, line) in enumerate(in_file):
        if (line_num == dim):
            break
        word = line.split()[0]
        word_dict[word] = line_num
    in_file.close()
    return word_dict

word_dict_700 = gen_word_dict(700,'word_freq_700.txt')

# test='/Users/wuxinheng/Documents/crawl_dogs/crawl_dogs_300_txt/affenpinscher'
# '/Users/wuxinheng/Documents/web_data_training/clean_data.py'
# os.listdir(test)
# for j in os.listdir(test):
#     save_file=os.path.join('/Users/wuxinheng/Documents/web_data_training/affenpinscher',j.split('.')[0]+'_feature.txt')
#     outfile = open(save_file,'w')
#     for line in open(os.path.join(test,j)):
#         words = line.lower().strip().split()
#         feature = [0]*dim
#         for word in words:
#             if word.isalpha() and word in word_dict:
#                 feature[word_dict[word]] += 1
#         for di in range(0, dim):
#             outfile.write(str(feature[di]) + '\n')
#     outfile.close()
os.makedirs('/Users/wuxinheng/Documents/crawl_dogs/dogs_txt_feature')
save_dir = '/Users/wuxinheng/Documents/crawl_dogs/dogs_txt_feature'
# feature extraction
for dog in os.listdir(root):
    if  not dog.startswith('.'):
        path = os.path.join(root,dog)
        for txt in os.listdir(path):
            if not txt.startswith('.'):
                file = os.path.join(path,txt)
                if not os.path.exists(os.path.join(save_dir,dog)):
                    os.makedirs(os.path.join(save_dir,dog))
                save_file = os.path.join(save_dir,dog,txt.split('.')[0]+'_feature.txt')
                outfile = open(save_file,'w')
                for line in open(os.path.join(path,txt)):
                    words =line.lower().strip().split()
                    feature =[0]*500
                    for word in words:
                        if word.isalpha() and word in word_dict_500:
                            feature[word_dict_500[word]] += 1
                    for di in range(0,500):
                        outfile.write(str(feature[di]) + '\n')
                outfile.close()
