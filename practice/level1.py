
#* Exercise 1 - Dataset Overview 

#! DUCKDB Exploration Exercise 

import duckdb
taxi_data = duckdb.read_parquet('data\\yellow_tripdata_2025-01.parquet')


## Total coloumn count 

# data = duckdb.sql("""
#     SELECT COUNT(*) FROM Information_Schema.columns
#     WHERE table_name = 'yellow_tripdata_2025-01'
#     LIMIT 3;
# """)
# print(data)

## Total rows count 

# data = duckdb.sql("""
#     SELECT COUNT(*) AS total_rows FROM taxi_data;
# """)
# print(data)

## Show Schema

# data = duckdb.sql("""
#     DESCRIBE taxi_data;
# """)

# print(data)

## Show First 20 rows 

# data = duckdb.sql("""
#     SELECT * FROM taxi_data
#     LIMIT 20;
# """)
# print(data)


#! POLARS Exploration Exercise 

import polars as pl 

## Read Parquet file 

po_df = pl.read_parquet('data\\yellow_tripdata_2025-01.parquet')

## Show Schema 

# print(po_df.describe());

## Show Shape

# print(po_df.shape);

## Show First 20 rows

# print(po_df.head(20));

#! PANDAS Exploration Exercise
 
import pandas as pd

## Read Parquet file 

pa_df = pd.read_parquet('data\\yellow_tripdata_2025-01.parquet');

## check info

# print(pa_df.info());

## Check shape

# print(pa_df.shape);

## Show first 20 rows

# print(pa_df.head(20));


#* Exercise 2 - Missing Values


#! DUCKDB

# COUNT(*) - count all rows in a table or coloumn
# COUNT(col_name) - count all non-NULL values in a specific column

# missing_data = duckdb.sql("""
#         SELECT 
#             COUNT(*) - COUNT(VendorID) AS missing_vendorid,
#             COUNT(*) - COUNT(tpep_pickup_datetime) AS missing_tpep_pickup_datetime,
#             COUNT(*) - COUNT(tpep_dropoff_datetime) AS missing_tpep_dropoff_datetime,
#             COUNT(*) - COUNT(passenger_count) AS missing_passenger_count,
#             COUNT(*) - COUNT(trip_distance) AS missing_trip_distance,
#             COUNT(*) - COUNT(RatecodeID) AS missing_rate_codeid,
#             COUNT(*) - COUNT(store_and_fwd_flag) AS missing_store_and_fwd_flag,
#             COUNT(*) - COUNT(PULocationID) AS missing_pu_locationid,
#             COUNT(*) - COUNT(DOLocationID) AS missing_do_locationid,
#             COUNT(*) - COUNT(payment_type) AS missing_payment_type,
#             COUNT(*) - COUNT(fare_amount) AS missing_fare_amount,
#             COUNT(*) - COUNT(extra) AS missing_extra,
#             COUNT(*) - COUNT(mta_tax) AS missing_mta_tax, 
#             COUNT(*) - COUNT(tip_amount) AS missing_tip_amount,
#             COUNT(*) - COUNT(tolls_amount) AS missing_tolls_amount,
#             COUNT(*) - COUNT(improvement_surcharge) AS missing_improvement_surcharge,
#             COUNT(*) - COUNT(total_amount) AS missing_total_amount,
#             COUNT(*) - COUNT(congestion_surcharge) AS missing_congestion_surcharge,
#             COUNT(*) - COUNT(Airport_fee) AS missing_airport_fee,
#             COUNT(*) - COUNT(cbd_congestion_fee) AS missing_cbd_congestion_fee

#             FROM taxi_data;

#  """)

# print(missing_data)

#! POLARS

# missing_data = po_df.null_count();

# print(missing_data)


#! PANDAS

# missing_data = pa_df.isna().sum();

# print(missing_data)


#* Exercise 3 - Basic Statistics

#! DUCKDB

# fare_amount_stats = duckdb.sql("""
#     SELECT MIN(fare_amount) AS min_fare_amount,
#            MAX(fare_amount) AS max_fare_amount,
#            AVG(fare_amount) AS mean_fare_amount,
#            MEDIAN(fare_amount) AS median_fare_amount,
#            STDDEV(fare_amount) AS stddev_fare_amount,
#         FROM taxi_data;
# """)

# print(fare_amount_stats)

# total_amount_stats = duckdb.sql("""
#     SELECT MIN(total_amount) AS min_total_amount,
#            MAX(total_amount) AS max_total_amount,
#            AVG(total_amount) AS mean_total_amount,
#            MEDIAN(total_amount) AS median_total_amount,
#            STDDEV(total_amount) AS stddev_total_amount,
#         FROM taxi_data;
# """)

# print(total_amount_stats)

# tip_amount_stats = duckdb.sql("""
#     SELECT MIN(tip_amount) AS min_tip_amount,
#            MAX(tip_amount) AS max_tip_amount,
#            AVG(tip_amount) AS mean_tip_amount,
#            MEDIAN(tip_amount) AS median_tip_amount,
#            STDDEV(tip_amount) AS stddev_tip_amount,
#         FROM taxi_data;
# """)

# print(tip_amount_stats)


# trip_distance_stats = duckdb.sql("""
#     SELECT MIN(trip_distance) AS min_trip_distance,
#            MAX(trip_distance) AS max_trip_distance,
#            AVG(trip_distance) AS mean_trip_distance,
#            MEDIAN(trip_distance) AS median_tript_distance,
#            STDDEV(trip_distance) AS stddev_trip_distance,
#         FROM taxi_data;
# """)

# print(trip_distance_stats)

#! POLARS

# stats_pl = po_df.select(
#     "fare_amount",
#     "total_amount",
#     "tip_amount",
#     "trip_distance"
# ).describe()

#   OR


# stats_pl = po_df.select(
#     pl.col("fare_amount").min().alias("min_fare_amount"),
#     pl.col("total_amount").min().alias("min_total_amount"),
#     pl.col("tip_amount").min().alias("min_tip_amount"),
#     pl.col("trip_distance").min().alias("min_trip_distance"),
#     pl.col("fare_amount").max().alias("max_fare_amount"),
#     pl.col("total_amount").max().alias("max_total_amount"),
#     pl.col("tip_amount").max().alias("max_tip_amount"),
#     pl.col("trip_distance").max().alias("max_trip_distance"),
#     pl.col("fare_amount").mean().alias("mean_fare_amount"),
#     pl.col("total_amount").mean().alias("mean_total_amount"),
#     pl.col("tip_amount").mean().alias("mean_tip_amount"),
#     pl.col("trip_distance").mean().alias("mean_trip_distance"),
#     pl.col("fare_amount").median().alias("median_fare_amount"),
#     pl.col("total_amount").median().alias("median_total_amount"),
#     pl.col("tip_amount").median().alias("median_tip_amount"),
#     pl.col("trip_distance").median().alias("median_trip_distance"),
#     pl.col("fare_amount").std().alias("stddev_fare_amount"),
#     pl.col("total_amount").std().alias("stddev_total_amount"),
#     pl.col("tip_amount").std().alias("stddev_tip_amount"),
#     pl.col("trip_distance").std().alias("stddev_trip_distance"),
# )

# print(stats_pl)


#! PANDAS

# cols = ["fare_amount", "total_amount", "tip_amount", "trip_distance"]

# pd_stats = pa_df[cols].agg(['min', 'max', 'mean', 'median', 'std']);

# OR 

# pd_stats = pa_df[
#                    cols
#                 ].describe()

# print(pd_stats)
