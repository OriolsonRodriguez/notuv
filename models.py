import numpy as np
import pandas as pd
import datetime

class Predictor:

    def __init__(self, model, data_goods, other_data=None):
        """model est une instance d'un modèle de prédiction
        data est un tableau pandas contenant toutes les données
        other_data est un tableau pandas contenant les éventuelles autres données
        """
        self.model = model
        self.data = data_goods
        self.other_data=other_data

    def predict_t(self,organisation,product,k=0):
        """ organisation is a string corresponding to the name of the organisation for which we want to predict
            product is a string corresponding to the name of the product from which we want to predict the quantity
            k is an int surch that the prediction is made at t_0 - k
        """
        data_sample = self.data[self.data['Organisation']==organisation]
        product_data=data_sample[data_sample['Product']==product]
        other_products_data=data_sample[data_sample['Product']!=product]

        stocks, _, _ = self.compute_stocks_out(product_data)
        return self.model.predict_next(stocks[k:],self.other_data,other_products_data)
    
    def compute_stocks_out(self,product_data):
        "compute for each day the number of goods out + padding for the empty days and sort by day"
        product_data['Scan Date']=pd.to_datetime(product_data['Scan Date'])

        max_date=product_data['Scan Date'].max()
        min_date=product_data['Scan Date'].min()
        length=(max_date-min_date).days + 1
        #.days round to the lower int

        #stocks[i] correspond au stock reçu au jour min_date + i
        stocks = [0]*length
        for i in range(len(product_data)):
            stocks[(product_data.loc[i,'Scan Date']-min_date).days] += product_data.loc[i,'Quantity']
        
        return stocks, max_date, min_date


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