from sklearn.base import TransformerMixin


class PercentageTransformer(TransformerMixin):
    """Transform points to percentage."""

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.transform(lambda row: row / row.sum(), axis=1)
