from datetime import datetime

from synthetic_gen import generator

goods_in_path='./Notuv_Denk_Pharma_1_Item_Registration.csv'
goods_out_path='./Notuv_Denk_Pharma_2_Goods_Out.csv'

num_records=1500

scan_date_i=datetime.strptime('29-JUN-2021 12:24:32', '%d-%b-%Y %H:%M:%S')
scan_date_f=datetime.strptime('29-JUN-2022 08:24:32', '%d-%b-%Y %H:%M:%S')

scan_ref=(1000, 5000)
supplier=['Bill Gates Foundation', 'Red Cross', 'WHO']

exp_date_i=datetime.strptime('29-OCT-2021 08:00:00', '%d-%b-%Y %H:%M:%S')
exp_date_f=datetime.strptime('28-JUL-2023 08:00:00', '%d-%b-%Y %H:%M:%S')

qty_mu=50
qty_sigma=60

organization=['Notuv - Denk Pharma']
scan_pnt_name_IN=['DMO_1001000']
scan_pnt_name_OUT=['DMO_1002000']
product=['Metformin']

generator=generator(num_records,(scan_date_i,scan_date_f), scan_ref, supplier, (exp_date_i, exp_date_f), 
    (qty_mu, qty_sigma), organization, scan_pnt_name_IN, product)

generator.run_pipeline()
generator.pd_goods_in.to_csv('./goods_in.csv', sep=',')