# Level 2 - Filtering & Aggregation

# * Exercise 4 - Payment Analysis

#! DUCKDB

import duckdb

taxi_data = duckdb.read_parquet("data\\yellow_tripdata_2025-01.parquet")

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

pl_df = pl.read_parquet("data\\yellow_tripdata_2025-01.parquet")

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

pd_df = pd.read_parquet("data\\yellow_tripdata_2025-01.parquet")

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

# avg_tip_amount = pd_df.groupby("payment_type")["tip_amount"].mean().reset_index(name="avg_tip_amount")
# print(avg_tip_amount)


# Ques 5 - Find highest fare by payment type

# highest_fare_amount = pd_df.groupby("payment_type")["fare_amount"].max().reset_index(name="highest_fare_amount")
# print(highest_fare_amount)


# * Exercise 5 - Vendor Comparison

#! DUCKDB

# Ques - 1 Compare vendor 1 vs vendor 2 in terms of number of total trips.

# total_trips_by_vendor = duckdb.sql("""
#         SELECT vendorid, COUNT(*) AS total_trips FROM taxi_data
#         WHERE vendorid IN (1, 2)
#         GROUP BY vendorid;
# """)

# print(total_trips_by_vendor)


# Ques - 2 Compare vendor 1 vs vendor 2 in terms of number of average distance.

# avg_distance_by_vendor = duckdb.sql("""
#         SELECT vendorid, AVG(trip_distance) AS avg_distance FROM taxi_data
#         WHERE vendorid IN (1, 2)
#         GROUP BY vendorid;
# """)

# print(avg_distance_by_vendor)


# Ques - 3 Compare vendor 1 vs vendor 2 in terms of number of average fare.

# avg_fare_by_vendor = duckdb.sql("""
#         SELECT vendorid, AVG(fare_amount) AS avg_fare FROM taxi_data
#         WHERE vendorid IN (1, 2)
#         GROUP BY vendorid;
# """)

# print(avg_fare_by_vendor)


# Ques - 4 Compare vendor 1 vs vendor 2 in terms of number of average tip.

# avg_tip_by_vendor = duckdb.sql("""
#         SELECT vendorid, AVG(tip_amount) AS avg_tip FROM taxi_data
#         WHERE vendorid IN (1, 2)
#         GROUP BY vendorid;
# """)

# print(avg_tip_by_vendor)


# Ques - 5 Compare vendor 1 vs vendor 2 in terms of number of average passenger.

# avg_passenger_by_vendor = duckdb.sql("""
#         SELECT vendorid, CAST(AVG(passenger_count) AS INTEGER) AS avg_passenger_count FROM taxi_data
#         WHERE vendorid IN (1, 2)
#         GROUP BY vendorid;
# """)

# print(avg_passenger_by_vendor)


#! POLARS

# Ques - 1 Compare vendor 1 vs vendor 2 in terms of number of total trips.

# total_trips_by_vendor = pl_df.filter(
#     pl.col("VendorID").is_in([1, 2])
# ).group_by("VendorID").agg(
#     pl.col("VendorID").count().alias("total_trips")
# )

# print(total_trips_by_vendor)


# Ques - 2 Compare vendor 1 vs vendor 2 in terms of number of average distance.

# avg_distance_by_vendor = pl_df.filter(
#     pl.col("VendorID").is_in([1, 2])
# ).group_by("VendorID").agg(
#     pl.col("trip_distance").mean().alias("avg_distance")
# )
# print(avg_distance_by_vendor)


# Ques - 3 Compare vendor 1 vs vendor 2 in terms of number of average fare.


# average_fare_by_vendor = (
#     pl_df.filter(pl.col("VendorID").is_in([1, 2]))
#     .group_by("VendorID")
#     .agg(pl.col("fare_amount").mean().alias("avg_fare_by_vendors"))
# )
# print(average_fare_by_vendor)


# Ques - 4 Compare vendor 1 vs vendor 2 in terms of number of average tip.


# average_tip_by_vendor = (
#     pl_df.filter(pl.col("VendorID").is_in([1, 2]))
#     .group_by("VendorID")
#     .agg(pl.col("tip_amount").mean().alias("avg_tip_by_vendors"))
# )
# print(average_tip_by_vendor)


# Ques - 5 Compare vendor 1 vs vendor 2 in terms of number of average passenger.

# average_passenger_count_by_vendor = (
#     pl_df.filter(pl.col("VendorID").is_in([1, 2]))
#     .group_by("VendorID")
#     .agg(
#         pl.col("passenger_count")
#         .mean()
#         .cast(pl.Int32)
#         .alias("avg_passenger_count_by_vendors")
#     )
# )

# print(average_passenger_count_by_vendor)


#! PANDAS

# Ques - 1 Compare vendor 1 vs vendor 2 in terms of number of total trips.

# total_trips_by_vendor = (
#     pd_df[pd_df["VendorID"].isin([1, 2])]
#     .groupby("VendorID")
#     .size()
#     .reset_index(name="total_trips_by_vendors")
# )


# print(total_trips_by_vendor)


# Ques - 2 Compare vendor 1 vs vendor 2 in terms of number of average distance.

# avg_distance_by_vendors = (pd_df
#     [pd_df["VendorID"].isin([1, 2])]
#     .groupby("VendorID")["trip_distance"]
#     .mean()
#     .reset_index(name="avg_distance_by_vendors"))

# print(avg_distance_by_vendors)


# Ques - 3 Compare vendor 1 vs vendor 2 in terms of number of average fare.

# avg_fare_by_vendors = (
#     pd_df[pd_df["VendorID"].isin([1, 2])]
#     .groupby("VendorID")["fare_amount"]
#     .mean()
#     .reset_index(name="avg_fare_by_vendors")
# )

# print(avg_fare_by_vendors)


# Ques - 4 Compare vendor 1 vs vendor 2 in terms of number of average tip.

# avg_tip_by_vendors = (
#     pd_df[pd_df["VendorID"].isin([1, 2])]
#     .groupby("VendorID")["tip_amount"]
#     .mean()
#     .reset_index(name="avg_tip_by_vendors")
# )
# print(avg_tip_by_vendors)


# Ques - 5 Compare vendor 1 vs vendor 2 in terms of number of average passenger.

avg_passenger_count_by_vendors = (
    pd_df[pd_df["VendorID"].isin([1, 2])]
    .groupby("VendorID")["passenger_count"]
    .mean()
    .astype(int)
    .reset_index(name="avg_passenger_count_by_vendors")
)
print(avg_passenger_count_by_vendors)
