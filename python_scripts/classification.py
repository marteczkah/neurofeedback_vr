from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from mne.decoding import CSP

class Classification:
    """Classification class that uses Common Spatial Pattern and 
    Linear Dicriminant Analysis to predict the state of the EGG data."""

    def __init__(self, num_classes):
        # the classifier elements: lda and csp
        self.csp = CSP(n_components=num_classes, reg=None, log=True, norm_trace=False)
        self.lda = LinearDiscriminantAnalysis()

    def train(self, X, y):
        transformed_data = self.csp.fit_transform(X, y)
        self.lda.fit(transformed_data, y)
    
    def predict(self, X):
        transformed_data = self.csp.transform(X)
        return self.lda.predict(transformed_data)
    
    def return_csp(self, X):
        return self.csp.transform(X)
    
    def plot_cps(self, epochs):
        self.csp.plot_patterns(epochs.info, ch_type="eeg", units="Patterns (AU)", size=1.5)


