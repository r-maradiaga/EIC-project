# EIC-project

## Installation 

Make a virtual environment, activate it, then run the following to get all of the necessary packages:

```bash 
pip install -r requirements.txt
```

A .env file is also needed to get the data from snowflake

## Example outputs

<img width="1249" height="625" alt="example_streamlit_ouput_for_customer_acquisition" src="https://github.com/user-attachments/assets/0989a7d6-18da-4475-9f2d-1c227f8d21c5" />

actual output from merging data from database: 

```bash
$ python true_customer_acquisition_cost.py 
        channel  customers_acquired  total_direct_spend  indirect_cost  converted_customers  staff_cost  technology_cost  returns_processing_cost  true_total_cost      true_cac
0        Direct                   4                0.00    3157.894737                  6.0       800.0            700.0                    500.0      5157.894737    859.649123
1         Email                   7              120.32    2105.263158                  4.0       400.0            600.0                    300.0      3525.583158    881.395789
2      Facebook                   3             1435.48       0.000000                  0.0      1200.0           1000.0                    800.0      4435.480000   4435.480000
3        Google                   6            10774.19    1578.947368                  3.0      1800.0           1500.0                   1000.0     16653.137368   5551.045789
4     Instagram                   3            14516.13       0.000000                  0.0      1500.0           1400.0                    900.0     18316.130000  18316.130000
5      Referral                   3                0.00       0.000000                  0.0         0.0              0.0                      0.0         0.000000      0.000000
6  Social Media                   3                0.00       0.000000                  0.0         0.0              0.0                      0.0         0.000000      0.000000
7        TikTok                   2             5000.00     526.315789                  1.0      1000.0           1200.0                   1100.0      8826.315789   8826.315789
```
