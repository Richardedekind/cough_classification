import numpy as np
import GPy
import pandas as pd

# based on the current evaluation loop, classifiers are assumed to have functions and fit and predict_proba as illustrated in this base class

# todo: include explanations about input and outpout variables formats so that someone who wants to make a classifier knows what is expected

# note that inputs to fit are a bit weird: xtrain is np array and ytrain is pandas. i think it would be better to convert ytrain to np array ints outside the classifier and not assume that classifiers have classes_ variable at all. for now i put the conversion in a separate function

class Classifier():

    def __init__(self):
        raise NotImplementedError
          
    def fit(self, xtrain, ytrain):
        raise NotImplementedError

    def predict_proba(self, xtest):
        raise NotImplementedError

    def convert_classes(self, classes):
        classids,names=pd.factorize(classes)
        self.classes_=names      
        return classids

# here is an example (note that the current logreg classifier can be used as is)
    
class GP_mini(Classifier):
    
    def __init__(self, kernel=None):
        self.kernel=kernel
        
    def set_default_kernel(self, dim):
        self.kernel=np.sum([GPy.kern.RBF(input_dim=1,active_dims=[ind]) for ind in range(dim)])
    
    def fit(self, xtrain, ytrain):
        
        # data conversion
        labels=self.convert_classes(ytrain)
        
        # check kernel
        if self.kernel is None: self.set_default_kernel(xtrain.shape[1])
        
        # train classifier
        self.model=GPy.models.GPClassification(xtrain,labels.reshape(-1,1),kernel=self.kernel.copy())
        self.model.optimize()
        
    def predict_proba(self, xtest):
        prob=self.model.predict(np.atleast_2d(xtest))[0]
        return np.concatenate((1-prob,prob),axis=1)
