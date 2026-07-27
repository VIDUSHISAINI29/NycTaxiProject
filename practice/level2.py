# Level 2 - Filtering & Aggregation

#* Exercise 4 - Payment Analysis 

#! DUCKDB 

import duckdb

taxi_data = duckdb.read_parquet('data\\yellow_tripdata_2025-01.parquet')

# Ques 1 - Find number of cash trips

# num_of_cash_trips = duckdb.sql("""
#     SELECT COUNT(*) AS cash_trips FROM taxi_data
#     WHERE payment_type = 2;
# """)
# print(num_of_cash_trips)


# Ques 2 - Find number of card trips

# num_of_card_trips = duckdb.sql("""
#     SELECT COUNT(*) AS card_trips FROM taxi_data
#     WHERE payment_type = 1;
# """)
# print(num_of_card_trips)


# Ques 3 - Find average fare by payment type

# avg_fare_amount_by_payment_type = duckdb.sql("""
#     SELECT payment_type, AVG(fare_amount) AS avg_fare_amount FROM taxi_data
#     GROUP BY payment_type;
# """)
# print(avg_fare_amount_by_payment_type)


# Ques 4 - Find average tip by payment type

# avg_tip_amount_by_payment_type = duckdb.sql("""
#     SELECT payment_type, AVG(tip_amount) AS avg_tip_amount FROM taxi_data
#     GROUP BY payment_type;
# """)
# print(avg_tip_amount_by_payment_type)


# Ques 5 - Find highest fare by payment type

# highest_fare_amount_by_payment_type = duckdb.sql("""
#     SELECT payment_type, MAX(fare_amount) AS highest_fare_amount FROM taxi_data
#     GROUP BY payment_type;
# """)
# print(highest_fare_amount_by_payment_type)


#! POLARS

import polars as pl

pl_df = pl.read_parquet('data\\yellow_tripdata_2025-01.parquet')    

# Ques 1 - Find number of cash trips

# cash_trips = pl_df.filter(pl.col("payment_type") == 2).height
# print('cash trips - ',cash_trips)


# Ques 2 - Find number of card trips

# card_trips = pl_df.filter(pl.col("payment_type") == 1).height
# print('card trips - ',card_trips)


# Ques 3 - Find average fare by payment type

    # avg_fare_amount = pl_df.group_by("payment_type").agg(
    #     pl.col("fare_amount").mean().alias("avg_fare_amount")
    # )
    # print('avg fare amount - ',avg_fare_amount)


# Ques 4 - Find average tip by payment type

# avg_tip_amount = pl_df.group_by("payment_type").agg(
#     pl.col("tip_amount").mean().alias("avg_tip_amount")
# )
# print('avg tip amount - ',avg_tip_amount)


# Ques 5 - Find highest fare by payment type

# highest_fare_amount = pl_df.group_by("payment_type").agg(
#     pl.col("fare_amount").max().alias("highest_fare_amount")
# )
# print('highest fare amount - ',highest_fare_amount)



#! PANDAS

import pandas as pd

pd_df = pd.read_parquet('data\\yellow_tripdata_2025-01.parquet')    

# Ques 1 - Find number of cash trips

# cash_trips = (pd_df["payment_type"] == 2).sum()
# print('cash trips - ',cash_trips)

# Ques 2 - Find number of card trips

# card_trips = (pd_df["payment_type"] == 1).sum()
# print('card trips - ',card_trips)


# Ques 3 - Find average fare by payment type

# avg_fare_amount = pd_df.groupby("payment_type")["fare_amount"].mean().reset_index(name="avg_fare_amount")
# print(avg_fare_amount)


# Ques 4 - Find average tip by payment type

avg_tip_amount = pd_df.groupby("payment_type")["tip_amount"].mean().reset_index(name="avg_tip_amount")
print(avg_tip_amount)


# Ques 5 - Find highest fare by payment type

# highest_fare_amount = pd_df.groupby("payment_type")["fare_amount"].max().reset_index(name="highest_fare_amount")
# print(highest_fare_amount)


#* Exercise 5 - Vendor Comparison  
