import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import statsmodels

class Predictor:

    def __init__(self, model, dataloader, other_data=None):
        """model est une instance d'un modèle de prédiction
        data est un tableau pandas contenant toutes les données
        other_data est un tableau pandas contenant les éventuelles autres données
        """
        self.model = model
        self.dataloader = dataloader
        self.other_data=other_data

    def predict_t(self,organisation,product,k=0):
        """ organisation is a string corresponding to the name of the organisation for which we want to predict
            product is a string corresponding to the name of the product from which we want to predict the quantity
            k is an int surch that the prediction is made at t_0 - k
        """
        stocks, _, _ = self.dataloader.compute_stocks_out(organisation,product)
        return self.model.predict_next(stocks[k:],self.other_data,[])  



class BasicModel:

    def __init__(self,hparams):
        self.hparams = hparams

    def f(self,demand):
        coeffs = self.hparams["coeffs_f"]
        """demand is a N list containing all the previous demand of a product"""
        return sum([demand[k]*coeffs[k] for k in range(len(coeffs))])

    def g(self,features):
        """features is a list containning the other features surch as weather"""
        return 0
    
    def h(self,other_products):
        """other_product is a dictionnary containing the demand list of the other products"""
        return 0
    
    def predict_next(self,demand,features,other_products):
        return self.f(demand)+self.g(features)+self.h(other_products)

class SarimaModel:

    def __init__(self,hparams):
        self.hparams = hparams

    def predict_next(self,demand,features,other_products):
        return
    
