import pickle

import numpy as np
import pandas as pd
import Utils
from keras.models import load_model

class lstm:
    def __init__(self):
        self.model = load_model('Vi_lstm_textclassifier.h5')
        print("Load model complete!")

    # Tf-idf
    def truncatedvectors(self, data, n_components=300):
        svd_ngram = pickle.load(open("svd_ngram.pickle", "rb"))
        return svd_ngram.transform(data)


    def tfidf(self, data):
        tfidf_vect_ngram = pickle.load(open("tfidf.pickle", "rb"))
        X_data_tfidf_ngram = tfidf_vect_ngram.transform(data)
        return self.truncatedvectors(X_data_tfidf_ngram)

    def predict_text(self, text='', classes=[]):
        processed_text = Utils.text_preprocessing(text)
        tfidf_text = self.tfidf(pd.Series(processed_text))
        tfidf_text.shape = (1, 300)
        y_pred = self.model.predict(tfidf_text, verbose = 0)
        y_pred_bool = np.argmax(y_pred, axis=1)
        y_pred_txt = classes[y_pred_bool[0]]
        return y_pred_txt