import numpy as np
import pandas as pd
import os.path
from abc import ABC, abstractmethod

class CSVLoader:

    def __init__(self,adress_in,adress_out):
        self.dataset_in=pd.read_csv(adress_in)
        self.dataset_out=pd.read_csv(adress_out)

        ##Deleting rows containing NaNs or empty spaces

        self.dataset_in.dropna(inplace=True)
        self.dataset_out.dropna(inplace=True)

        #Sorting by date

        self.dataset_out.sort_values(by="Scan Date")
        self.dataset_in.sort_values(by="Scan Date")



    def compute_stocks_out(self,organisation,product):
        """compute for each day the number of goods out + padding for the empty days and sort by day
        the output is a list, stocks[i] correspond au stock reçu au jour min_date + i"""

        data_sample = self.dataset_out[self.dataset_out['Organisation']==organisation]
        product_data=data_sample[data_sample['Product']==product]
        #other_products_data=data_sample[data_sample['Product']!=product]

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
    
    def compute_stocks_in(self,organisation,product):
        """compute for each day the number of goods out + padding for the empty days and sort by day
        the output is a list, stocks[i] correspond au stock reçu au jour min_date + i"""

        data_sample = self.dataset_in[self.dataset_in['Organisation']==organisation]
        product_data=data_sample[data_sample['Product']==product]
        #other_products_data=data_sample[data_sample['Product']!=product]

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
