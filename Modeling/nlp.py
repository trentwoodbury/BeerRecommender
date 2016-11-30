from nltk.corpus import stopwords
import pickle
from sklearn.decomposition import NMF
from sklearn.feature_extraction.text import TfidfVectorizer

def get_dataframe(filepath):
    #Load data
    data = pickle.load(open(filepath))
    return data

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print "Topic #{}:".format(topic_idx)
        print " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        print '\n'

def nmf_descriptions(df):
    #INPUT: dataframe of beer info
    #OUTPUT: NMF of beer descriptions
    corpus = df['description']
    sw = stopwords.words('english')
    sw.extend(['hoppy', 'beer'])
    tf = TfidfVectorizer(max_df = .9, stop_words = sw).fit_transform(corpus)
    feature_names = tf.get_feature_names()

    nmf = NMF(n_components = 10, l1_ratio = 0.5).fit(df)

    return nmf, feature_names


if __name__ == "__main__":
    df = get_dataframe('../Data/beer_data_final.pkl')
    nmf, feature_names = nmf_descriptions(df)
    print_top_words(nmf, feature_names, 10 )
