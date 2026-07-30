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

# Create new coloumns trip_duratin_minutes, average_speed, fare_per_mile, tip_percentage_, is_Weekend, is_night_trip, is_airport_trip

#! DUCKDB

# new_cols = duckdb.sql("""
#         SELECT *,
#        DATEDIFF('minute', tpep_pickup_datetime, tpep_dropoff_datetime) AS trip_duration_minutes,
#        ROUND((DATEDIFF('minute', tpep_pickup_datetime, tpep_dropoff_datetime) / 60) / (trip_distance * 1.609), 2) AS avg_speed_km_per_hr,
#        ROUND((fare_amount / trip_distance), 2) AS fare_per_mile,
#        ROUND(((tip_amount / fare_amount) * 100), 2) AS tip_percentage,
#        Airport_fee != 0 AS is_airport_trip,
#        CASE
#         WHEN DAYOFWEEK(tpep_pickup_datetime) IN (0, 6) THEN TRUE
#         ELSE FALSE
#         END AS is_weekend,CASE
#         WHEN EXTRACT(HOUR FROM tpep_pickup_datetime) >= 22
#          OR EXTRACT(HOUR FROM tpep_pickup_datetime) < 6
#         THEN TRUE
#         ELSE FALSE
#         END AS is_night_trip
#             FROM taxi_data
#         WHERE tpep_pickup_datetime < tpep_dropoff_datetime
#         LIMIT 5;
# """)

# print(new_cols)


#! POLARS


# new_cols = pl_df.select(
#     (pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime"))
#     .dt.total_minutes()
#     .alias("trip_duration_minutes"),
#     (
#         (pl.col("trip_distance") * 1.609)
#         / (
#             (
#                 pl.col("tpep_dropoff_datetime") - pl.col("tpep_pickup_datetime")
#             ).dt.total_minutes()
#             / 60
#         )
#     )
#     .round(2)
#     .alias("average_speed_km_per_hour"),
#     (pl.col("fare_amount") / pl.col("trip_distance")).round(2).alias("fare_per_mile"),
#     ((pl.col("tip_amount") / pl.col("fare_amount")) * 100)
#     .round(2)
#     .alias("tip_percentage"),
#     pl.when(pl.col("tpep_pickup_datetime").dt.weekday().is_in([5, 6]))
#     .then(True)
#     .otherwise(False)
#     .alias("is_weekend"),
#     pl.when(
#         pl.col("Airport_fee") != 0
#     )
#     .then(True)
#     .otherwise(False)
#     .alias("is_airport_trip"),
#     ((pl.col('tpep_pickup_datetime').dt.hour() >= 22) | (pl.col('tpep_pickup_datetime').dt.hour() < 6)).alias('is_night_trip')
# )

# print(new_cols)


#! PANDAS

import numpy as np

new_cols = (
    pd_df.assign(
        trip_duration_minutes = ((pd_df["tpep_pickup_datetime"] - pd_df["tpep_dropoff_datetime"]).dt.total_seconds() / 60),
        avg_speed = ((pd_df["trip_distance"] * 1.609) / ((pd_df["tpep_pickup_datetime"] - pd_df["tpep_dropoff_datetime"]).dt.total_seconds() / 3600)),
        fare_per_mile = (pd_df["trip_distance"] / pd_df["fare_amount"]).round(2),
        tip_percentage = ((pd_df["tip_amount"] / pd_df["fare_amount"]) * 100).round(2),
        is_airport_trip = np.where(
            pd_df["Airport_fee"] != 0, True, False
        ),
        is_weekend = np.where(
            pd_df["tpep_pickup_datetime"].dt.weekday.isin([5, 6]), True, False
        ), 
        is_night_trip = np.where(
            ((pd_df["tpep_pickup_datetime"].dt.hour >= 22) | (pd_df["tpep_pickup_datetime"].dt.hour < 6)), True, False
        )
    )
)

print(new_cols)

