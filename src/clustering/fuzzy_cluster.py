import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.mixture import GaussianMixture


class FuzzyClusterer:

    def __init__(self, n_clusters=12, pca_components=50):
        """
        Soft clustering using Gaussian Mixture Models.
        Each document receives a probability distribution across clusters.
        """

        self.n_clusters = n_clusters
        self.pca_components = pca_components

        self.scaler = StandardScaler()
        self.pca = PCA(n_components=pca_components)

        self.model = GaussianMixture(
            n_components=n_clusters,
            covariance_type="full",
            random_state=42
        )

        self.membership = None

    def fit(self, embeddings):

        # normalize
        scaled = self.scaler.fit_transform(embeddings)

        # reduce dimension
        reduced = self.pca.fit_transform(scaled)

        # train mixture model
        self.model.fit(reduced)

        # get soft cluster memberships
        self.membership = self.model.predict_proba(reduced).T

        return self.membership

    def dominant_cluster(self, doc_index):

        return np.argmax(self.membership[:, doc_index])