import gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from prompt_toolkit.key_binding.bindings.named_commands import self_insert


# class lda:
#     def __init__(self, datanews=[]):
#         self.datanews = datanews.apply(lambda x: x.split()).tolist()
#         self.dictionary = gensim.corpora.Dictionary([self.datanews])
#         self.dictionary.filter_extremes(no_below=15, no_above=0.1, keep_n=100000)
#         self.bow_corpus = [self.dictionary.doc2bow(doc) for doc in datanews]
#         self.tfidf = gensim.models.TfidfModel(self.bow_corpus)
#         self.corpus_tfidf = self.tfidf[self.bow_corpus]

def topic_modeling(datanews=[], corpus_tfidf=[], dictionary=dict, bow_corpus=[]):
    if len(datanews) < 5: num_topics = 1
    else: num_topics = round(len(datanews) / 5)
    lda_model = gensim.models.LdaMulticore(corpus_tfidf, num_topics=num_topics, id2word=dictionary, passes=10, workers=2)
    topic_dict = dict()
    for idx, topic in lda_model.show_topics(formatted=False, num_words=10):
        words = '|'.join([w[0] for w in topic])
        topic_dict[idx] = words
    topic_modeling, score = [], []
    for idx, news in enumerate(datanews):
        score.append(lda_model[bow_corpus[idx]][0][1])
        topic_modeling.append(topic_dict.get(lda_model[bow_corpus[idx]][0][0]))
    return (topic_modeling, score)

