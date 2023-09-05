import re
import string

from pyvi.ViTokenizer import ViTokenizer


def text_preprocessing(text=''):
    text = text.lower()
    text = text.translate(text.maketrans(string.punctuation, ' '*len(string.punctuation)))
    text = re.sub('\s+', ' ', text)
    return ViTokenizer.tokenize(text)

def list_preprocessing(list=[]):
    preprocessed_list = []
    for content in list:
        preprocessed_text = text_preprocessing(content)
        preprocessed_list.append(preprocessed_text)
    return preprocessed_list