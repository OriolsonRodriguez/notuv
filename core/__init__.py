"""

I) Description of the data input

Id => Identification key
Name => Name of the product
W=> Quantity
Expiracy = Out-of-date time
(x,y) => geolocalisation
Date => Date of the scan
State => Delivered (demand) ,wasted (out-of-date) , stock

II) Data input

For each product j
Demand_t = f[demand_(t-1)+demand_(t-2)+...+demand(t-k)] + g(others variables such as weather) + h(demand for the other products in t-1...t-k) + error

III) Model

=> We should use the most simple model since we do not have the real data. 


"""

