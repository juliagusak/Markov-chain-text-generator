import os

repository_path = os.path.abspath('/media/julia/My Passport/semestr1/Python/TextGenerator_new')
corpus_path = repository_path + '/lib'
stopwords_path = repository_path + '/lib/stopwords.txt'
word_dict_path = '{}/save_word_dict.pkl'.format(repository_path)
word_frequency_dict_path = '{}/save_word_frequency_dict.pkl'.format(repository_path)
generated_text_path = 'generated_text.txt'
