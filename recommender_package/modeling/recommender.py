''' Authors: Dylan Albrecht
             Trent Woodbury

    Some models for recommendation.  So far contains a KNN model.
'''
import numpy as np
from sklearn.neighbors import NearestNeighbors

from ..utils.modeling import normalize
from ..utils.modeling import vectorize


class BeerTransformer(object):
    def __init__(self, vectorizer=None, normalizer=None):
        self.vectorizer = vectorizer
        self.normalizer = normalizer

    def fit(self, X):
        tmp_X, self.vectorizer = vectorize(X)
        _, self.normalizer = normalize(tmp_X)

    def transform(self, X):
        if not self.vectorizer or not self.normalizer:
            raise ValueError("Must fit first!")

        tmp_X, _ = vectorize(X, vectorizer=self.vectorizer)
        tmp_X, _ = normalize(tmp_X, normalizer=self.normalizer)

        return tmp_X

    def fit_transform(self, X):
        tmp_X, self.vectorizer = vectorize(X)
        tmp_X, self.normalizer = normalize(tmp_X)

        return tmp_X


class BeerKNN(object):
    def __init__(self, index=None, n_neighbors=6, algorithm='brute'):
        self.index=index
        self.n_neighbors = n_neighbors
        self.algorithm = algorithm
        self._knn_model = None
        self._X = None

    def fit(self, X):
        if self.index is None:
            self.index = np.arange(len(X))

        self._X = X
        self._knn_model = NearestNeighbors(n_neighbors=self.n_neighbors,
                                           algorithm=self.algorithm).fit(X)


    def predict(self, x):
        dist, ind = self._knn_model.kneighbors(x)

        return self.index[ind[0]]



##############
# End of File
##############
