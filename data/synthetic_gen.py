import random

from datetime import timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class generator():
    '''
    This class takes two csv files: good in and goods out and fill it in with with synthetic data.
    '''

    def __init__(self, num_records:int, scan_date_rng:tuple, scan_date_out_rng:tuple, scan_ref:tuple , supplier:list, exp_dates_rng:tuple, qty:tuple, 
        organization=['Notuv - Denk Pharma'], scan_pnt_name_IN=['DMO_1001000'], scan_pnt_name_OUT=['DMO_1002000'],product=['Metformin']):
        
        self.num_records=num_records
        self.scan_date_rng=scan_date_rng
        self.scan_date_out_rng=scan_date_out_rng
        self.scan_ref=scan_ref
        self.supplier=supplier
        self.exp_dates_rng=exp_dates_rng
        self.qty=qty 
        self.organization=organization
        self.scan_pnt_name_IN=scan_pnt_name_IN
        self.scan_pnt_name_OUT=scan_pnt_name_OUT
        self.product=product
        self.headers_in=None
        self.headers_out=None
        self.headers_inventory=None
        self.pd_goods_in=None
        self.pd_goods_out=None
        self.pd_inventory=None

    def create_dataFrames(self):
        self.headers_in=['Organisation', 'Scan Date', 'Scan Point Name', 'Scan Reference', 'Supplier Name',
            'Product', 'Expiration Date', 'Quantity']
        self.headers_out=self.headers_in.copy()
        self.headers_out.append('Goods wasted')
        self.headers_inventory=['Organisation', 'date_IN','Scan Reference', 'qty', 'qty_wasted', 'qty_new']

        self.pd_goods_in=pd.DataFrame(columns=self.headers_in)
        self.pd_goods_out=pd.DataFrame(columns=self.headers_out)
        self.pd_inventory=pd.DataFrame(columns=self.pd_inventory)
        return

    def compute_dateList(self, days_between_dates, mode='IN'):
        dates_list=[]
        if mode=='IN':
            initial_date=self.scan_date_rng[0]
        else:
            initial_date=self.scan_date_out_rng[0]
        for i in range(self.num_records):
            random_second = random.randrange(86400)
            random_day = random.randrange(days_between_dates)
            dates_list.append(initial_date + timedelta(seconds=random_second)+timedelta(days=random_day))

        dates_list.sort()
        return dates_list


    def fill_in_scan_dates(self, mode='IN'):
        '''
        IN:This is independent of all other vars
        OUT:This is dependent of dates in: initial date + one week (no inventory, no party)
        '''
        
        if mode=='IN':
            time_between_dates = self.scan_date_rng[1] - self.scan_date_rng[0]
        else:
            time_between_dates = self.scan_date_out_rng[1] - self.scan_date_out_rng[0]
        days_between_dates = time_between_dates.days
        
        dates_list=self.compute_dateList(days_between_dates, mode)
        if mode=='IN':
            self.pd_goods_in['Scan Date']=pd.Series(dates_list)
        else:
            self.pd_goods_out['Scan Date']=pd.Series(dates_list)
        return


    def fill_in_static_vars_IN(self):
        '''
        This will fill in static vars: organization, scan point name, suppliers
        '''
        organisation_list=[]
        scan_ptn_list=[]
        suppliers_list=[]
        product_list=[]

        for i in range(self.num_records):
            organisation_list.append(random.choice(self.organization))
            scan_ptn_list.append(random.choice(self.scan_pnt_name_IN))
            suppliers_list.append(random.choice(self.supplier))
            product_list.append(random.choice(self.product))
        
        self.pd_goods_in['Organisation']=pd.Series(organisation_list)
        self.pd_goods_in['Scan Point Name']=pd.Series(scan_ptn_list)
        self.pd_goods_in['Supplier Name']=pd.Series(suppliers_list)
        self.pd_goods_in['Product']=pd.Series(product_list)
        return

    def fill_in_scan_refs_IN(self):
        '''
        for scan dates according to given scan_ref range
        '''
        x=np.array(list(range(self.scan_ref[0], self.scan_ref[1])))
        np.random.shuffle(x)
        scan_refs_list=list(x[0:self.num_records])

        self.pd_goods_in['Scan Reference']=pd.Series(scan_refs_list)
        
        return

    def fill_in_exp_date_IN(self):
        '''
        done randomly according to input range. Does not matter which product
        '''
        dates_list=[]
        time_between_dates = self.exp_dates_rng[1] - self.exp_dates_rng[0]
        days_between_dates = time_between_dates.days
        for i in range(self.num_records):
            random_days = random.randrange(days_between_dates)
            dates_list.append(self.exp_dates_rng[0] + timedelta(days=random_days))

        self.pd_goods_in['Expiration Date']=pd.Series(dates_list)
        return

    def fill_in_qty_IN(self):
        '''
        for goods in is is done randomly. for goods out randomly with upper bound qty not higher than in qty for 
        that product
        '''
        qty_list=np.random.normal(self.qty[0], self.qty[1], self.num_records).astype(int)
        qty_list[qty_list<=0]=1
        qty_list=list(qty_list)
        self.pd_goods_in['Quantity']=pd.Series(qty_list)
        return

    def plot_timeQty(self, mode='IN', product='Metformin'):
        '''
        plot time vs qty for either IN or OUT
        '''

        time_IN=self.pd_goods_in['Scan Date'].to_numpy()
        qty_cumsum_IN=self.pd_goods_in['Quantity'].cumsum().to_numpy()
        qty_per_date_IN=self.pd_goods_in['Quantity'].to_numpy()

        time_OUT=self.pd_goods_out['Scan Date'].to_numpy()
        qty_cumsum_OUT=self.pd_goods_out['Quantity'].cumsum().to_numpy()
        qty_per_date_OUT=self.pd_goods_out['Quantity'].to_numpy()

        
        plt.plot(time_IN,qty_cumsum_IN, label='goods IN')
        plt.plot(time_OUT,qty_cumsum_OUT, label='goods OUT')
        plt.title('Cumulative Sum')
        plt.show()
        

        plt.plot(time_IN,qty_per_date_IN , label='goods IN')
        plt.plot(time_OUT,qty_per_date_OUT, label='goods OUT')
        plt.title('Goods vs time')
        plt.show()
        return

    def update_inventory_expired(self, date):
        temp_frame=self.pd_inventory
        self.pd_inventory.loc[self.pd_inventory['Expiration Date']<=date,'qty_wasted']=temp_frame['qty']
        self.pd_inventory.loc[self.pd_inventory['Expiration Date']<=date, 'qty']=0
        return

    def fill_in_goods_OUT(self):
        '''
        last step where it checks pd_goods_in for scan ref and expiration date. Make update step to pd_inventory
        '''
        scan_reference=[]
        supplier_names=[]
        products=[]
        exp_dates=[]
        qty_list=[]
        goods_wasted=[]
        organisation_list=[]
        scan_ptn_list=[]

        for idx, row in self.pd_goods_out.iterrows():
            self.update_inventory_expired(row['Scan Date'])
            for i in range(len(self.pd_inventory['Scan Reference'])):
                rand_id=int(random.choice(list(self.pd_inventory['Scan Reference'].to_numpy())))
                qty=int(self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['qty'].to_numpy())
                date_IN=self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['date_IN'].head().to_list()[0]
                
                if qty>=1 and date_IN<row['Scan Date']:
                    rnd_qty=random.randint(1, qty)
                    scan_reference.append(int(self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['Scan Reference'].to_numpy()))
                    supplier_names.append(str(self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['Supplier Name'].to_numpy()[0]))
                    products.append(str(self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['Product'].to_numpy()[0]))
                    exp_dates.append(str(self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['Expiration Date'].head().to_list()[0]))
                    qty_list.append(int(rnd_qty))
                    goods_wasted.append('N')
                    organisation_list.append(str(self.pd_inventory[self.pd_inventory['Scan Reference']==rand_id]['Organisation'].to_numpy()[0]))
                    scan_ptn_list.append(self.scan_pnt_name_OUT[0])
                    self.pd_inventory.loc[self.pd_inventory['Scan Reference']==rand_id,'qty']=qty-rnd_qty
                    break
        self.pd_goods_out['Scan Reference']=pd.Series(scan_reference)
        self.pd_goods_out['Supplier Name']=pd.Series(supplier_names)
        self.pd_goods_out['Product']=pd.Series(products)
        self.pd_goods_out['Expiration Date']=pd.Series(exp_dates)
        self.pd_goods_out['Quantity']=pd.Series(qty_list)
        self.pd_goods_out['Goods wasted']=pd.Series(goods_wasted)
        self.pd_goods_out['Organisation']=pd.Series(organisation_list)
        self.pd_goods_out['Scan Point Name']=pd.Series(scan_ptn_list)
        return
    
    def fill_in_already_expired_to_OUT(self):
        '''
        Adds expired medicines to pd OUT and put them as scan out
        '''
        scan_reference=[]
        supplier_names=[]
        products=[]
        exp_dates=[]
        qty_list=[]
        goods_wasted=[]
        organisation_list=[]
        scan_ptn_list=[]
        scan_date=[]
        pd_temp=pd.DataFrame(columns=self.headers_out)
        for idx, row in self.pd_inventory.iterrows():
            if row['qty']!=0:
                scan_reference.append(int(row['Scan Reference']))
                supplier_names.append(row['Supplier Name'])
                products.append(row['Product'])
                exp_dates.append(row['Expiration Date'])
                scan_date.append(row['Expiration Date'])
                qty_list.append(row['qty'])
                goods_wasted.append('Y')
                organisation_list.append(row['Organisation'])
                scan_ptn_list.append(self.scan_pnt_name_OUT[0])
                
        pd_temp['Scan Reference']=pd.Series(scan_reference)
        pd_temp['Supplier Name']=pd.Series(supplier_names)
        pd_temp['Product']=pd.Series(products)
        pd_temp['Expiration Date']=pd.Series(exp_dates)
        pd_temp['Quantity']=pd.Series(qty_list)
        pd_temp['Goods wasted']=pd.Series(goods_wasted)
        pd_temp['Organisation']=pd.Series(organisation_list)
        pd_temp['Scan Point Name']=pd.Series(scan_ptn_list)
        pd_temp['Scan Date']=pd.Series(scan_date)

        self.pd_goods_out=self.pd_goods_out.append(pd_temp, ignore_index=True)
        self.pd_goods_out=self.pd_goods_out.sort_values(by='Scan Date')
        self.pd_goods_out.reset_index(inplace=True)
        del self.pd_goods_out['index']
        return

    def compute_pd_inventory(self):
        '''
        we use the third dataframe to keep track of the actual stock per day per product
        '''
        #['Scan Reference', 'qty_wasted', 'qty_new']
        self.pd_inventory['date_IN']=self.pd_goods_in['Scan Date']
        self.pd_inventory['Scan Reference']=self.pd_goods_in['Scan Reference']
        self.pd_inventory['qty']=self.pd_goods_in['Quantity']
        self.pd_inventory['qty_wasted']=0
        self.pd_inventory['Expiration Date']=self.pd_goods_in['Expiration Date']
        self.pd_inventory['Supplier Name']=self.pd_goods_in['Supplier Name']
        self.pd_inventory['Product']=self.pd_goods_in['Product']
        self.pd_inventory['Organisation']=self.pd_goods_in['Organisation']
        return

    def run_pipeline(self):
        '''
        run all functions
        '''
        self.create_dataFrames()
        self.fill_in_scan_dates(mode='IN')
        self.fill_in_static_vars_IN()
        self.fill_in_scan_refs_IN()
        self.fill_in_exp_date_IN()
        self.fill_in_qty_IN()
        self.pd_goods_in.to_csv('./goods_IN.csv', sep=',')

        self.compute_pd_inventory() #call here once we have scan_dates OUT

        
        self.fill_in_scan_dates(mode='OUT')
        self.fill_in_goods_OUT()
        self.fill_in_already_expired_to_OUT()
        self.pd_goods_out.to_csv('./goods_OUT.csv', sep=',')
        

        self.plot_timeQty(mode='IN')


