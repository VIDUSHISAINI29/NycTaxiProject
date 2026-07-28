# Level 2 - Time Analysis

# * Exercise 7 - Trip by Hour

# Show trips by hours and Avg fare by hours

#! DUCKDB

import duckdb

taxi_data = duckdb.read_parquet("data\\yellow_tripdata_2025-01.parquet")

# trips_by_hour = duckdb.sql(
#     """ SELECT  DATEDIFF('hour', tpep_pickup_datetime, tpep_dropoff_datetime) AS hour_diff, COUNT(*) AS trip_count  FROM taxi_data
#   WHERE tpep_pickup_datetime < tpep_dropoff_datetime
# 	GROUP BY hour_diff
#   ORDER BY hour_diff;
# """
# )

# print(trips_by_hour)

# avg_fare_by_hours = duckdb.sql("""
#     SELECT  DATEDIFF('hour', tpep_pickup_datetime, tpep_dropoff_datetime) AS hour_diff, AVG(fare_amount) AS avg_fare_amount  FROM taxi_data
#    WHERE tpep_pickup_datetime < tpep_dropoff_datetime
#  	GROUP BY hour_diff
#    ORDER BY hour_diff;
# """)

# print(avg_fare_by_hours)


#! POLARS

import polars as pl

pl_df = pl.read_parquet("data\\yellow_tripdata_2025-01.parquet")

# trips_by_hour = (
#     pl_df.with_columns(
#         (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime"))
#         .dt.total_hours()
#         .alias("hour_diff")
#     )
#     .filter(pl.col("tpep_pickup_datetime") < pl.col("tpep_dropoff_datetime"))
#     .group_by("hour_diff")
#     .agg(pl.col("VendorID").count().alias('trip_count'))
#     .sort('hour_diff')
# )

# print(trips_by_hour)

# avg_fare_by_hour = (
#     pl_df.with_columns(
#         (pl.col('tpep_dropoff_datetime') - pl.col('tpep_pickup_datetime')).dt.total_hours().alias('hour_diff')
#     )
#     .filter(
#         pl.col('tpep_dropoff_datetime') > pl.col('tpep_pickup_datetime')
#     )
#     .group_by('hour_diff')
#     .agg(pl.col('fare_amount').mean().alias('avg_fare_amount_by_hour'))
#     .sort('hour_diff')
# )

# print(avg_fare_by_hour)


#! PANDAS

import pandas as pd

pd_df = pd.read_parquet("data\\yellow_tripdata_2025-01.parquet")

# trips_by_hour = (
#     pd_df.assign(
#         hour_diff=(
#             pd_df["tpep_dropoff_datetime"] - pd_df["tpep_pickup_datetime"]
#         ).dt.total_seconds()
#         / 3600
#     )
#     .loc[lambda df: df["tpep_dropoff_datetime"] > df["tpep_pickup_datetime"]]
#     .groupby("hour_diff")
#     .size()
#     .reset_index(name="trip_count")
#     .sort_values("hour_diff")
# )

# print(trips_by_hour)

# avg_fare_by_hour = (
#     pd_df.assign(
#         hour_diff=((
#             pd_df["tpep_dropoff_datetime"] - pd_df["tpep_pickup_datetime"]
#         ).dt.total_seconds()
#         / 3600).astype(int)
#     )
#     .loc[lambda df: df["tpep_dropoff_datetime"] > df["tpep_pickup_datetime"]]
#     .groupby("hour_diff")["fare_amount"]
#     .mean()
#     .reset_index(name="avg_fare_amount_by_hour")
#     .sort_values("hour_diff")
# )

# print(avg_fare_by_hour)




# * Exercise 8 - Trip Duration

