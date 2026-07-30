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

# new_cols = (
#     pd_df.assign(
#         trip_duration_minutes = ((pd_df["tpep_pickup_datetime"] - pd_df["tpep_dropoff_datetime"]).dt.total_seconds() / 60),
#         avg_speed = ((pd_df["trip_distance"] * 1.609) / ((pd_df["tpep_pickup_datetime"] - pd_df["tpep_dropoff_datetime"]).dt.total_seconds() / 3600)),
#         fare_per_mile = (pd_df["trip_distance"] / pd_df["fare_amount"]).round(2),
#         tip_percentage = ((pd_df["tip_amount"] / pd_df["fare_amount"]) * 100).round(2),
#         is_airport_trip = np.where(
#             pd_df["Airport_fee"] != 0, True, False
#         ),
#         is_weekend = np.where(
#             pd_df["tpep_pickup_datetime"].dt.weekday.isin([5, 6]), True, False
#         ),
#         is_night_trip = np.where(
#             ((pd_df["tpep_pickup_datetime"].dt.hour >= 22) | (pd_df["tpep_pickup_datetime"].dt.hour < 6)), True, False
#         )
#     )
# )

# print(new_cols)


# * Exercise 9 - Business Questions

#! DUCKDB

# Ques 1 - Which Vendor earns more

# vendor_with_more_earning = duckdb.sql("""
#     SELECT VendorID, ROUND(SUM(total_amount), 2) AS total_earning FROM taxi_data
#     GROUP BY VendorID
#     ORDER BY total_earning DESC
#     LIMIT 1;
# """)

# print(vendor_with_more_earning)


# Ques 2 - Which Payment type gives highest tips

# payment_type_with_highest_tip = duckdb.sql("""
#     SELECT payment_type, MAX(tip_amount) AS highest_tip FROM taxi_data
#     GROUP BY payment_type
#     ORDER BY highest_tip DESC
#     LIMIT 1;
# """)

# print(payment_type_with_highest_tip)


# Ques 3 - Average Revenue per trip

# avg_revenue_per_trip = duckdb.sql("""
#     SELECT ROUND((SUM(total_amount) / COUNT(*)), 2) AS avg_revenue_per_trip FROM taxi_data
# """)

# print(avg_revenue_per_trip)


# Ques 4 - Most common pickup location

# most_common_pu_location = duckdb.sql("""
#     SELECT COUNT(*) AS count_of_location, PULocationID FROM taxi_data
#     GROUP BY PULocationID
#     ORDER BY count_of_location DESC
#     LIMIT 1;
# """)

# print(most_common_pu_location)


# Ques 5 - Most common dropoff location

# most_common_do_location = duckdb.sql("""
#     SELECT COUNT(*) AS count_of_location, DOLocationID    FROM taxi_data
#     GROUP BY DOLocationID
#     ORDER BY count_of_location DESC
#     LIMIT 1;
# """)

# print(most_common_do_location)


# Ques 6 - Airport trips vs non-airport trips

# airport_vs_non_airport_trip = duckdb.sql("""
#     SELECT
#         CASE
#          WHEN Airport_fee != 0 THEN TRUE
#          ELSE FALSE
#          END AS is_airport_trip,
#          COUNT(*) AS total_trips
#            FROM taxi_data
#     GROUP BY is_airport_trip
# """)

# print(airport_vs_non_airport_trip)


# Ques 7 - Longest Average trip distance

# longest_trip_distance = duckdb.sql("""
#     SELECT MAX(trip_distance) AS longest_trip_diance FROM taxi_data

# """)

# print(longest_trip_distance)


# Ques 8 - Highest Average fare

# higest_fare = duckdb.sql("""
#     SELECT MAX(fare_amount) AS highest_avg_fare FROM taxi_data

# """)

# print(higest_fare)


#! POLARS


# Ques 1 - Which Vendor earns more

# most_earning_vendor = pl_df.group_by("VendorID").agg(
#     pl.col('total_amount').sum().alias('total_earning')
# ).sort('total_earning', descending=True).head(1)

# print(most_earning_vendor)
# print(most_earning_vendor.to_pandas())


# Ques 2 - Which payment type gives highest tip

# highest_tip_paying_payment_type = pl_df.group_by("payment_type").agg(
#     pl.col('tip_amount').max().alias('highest_tip')
# ).sort('highest_tip', descending=True).head(1)

# print(highest_tip_paying_payment_type)


# Ques 3 - Average revenue per trip

# avg_revenue_per_trip = pl_df.select(
#     pl.col('total_amount').mean().round(2).alias("avg_revenue_per_trip")
# )

# print(avg_revenue_per_trip)


# Ques 4 - Most common pickup location

# most_common_pu_location = pl_df.group_by('PULocationID').agg(
#     pl.col('trip_distance').count().alias("count_of_trips")
# ).sort('count_of_trips', descending=True).head(1)

# print(most_common_pu_location)


# Ques 5 - Most common dropoff location

# most_common_do_location = pl_df.group_by('DOLocationID').agg(
#     pl.len().alias("count_of_trips")
# ).sort('count_of_trips', descending=True).head(1)

# print(most_common_do_location)


# Ques 6 - Airport vs non- airport trip

# airport_vs_non_airport_trip = pl_df.group_by(
#     (pl.col("Airport_fee") != 0).alias("is_airport_trip")
# ).agg(pl.len().alias("total_trips"))

# print(airport_vs_non_airport_trip)


# Ques 7 - Longest trip distance

# longest_trip_distance = pl_df.select(
#         pl.col('trip_distance').max().alias('longest_trip_distance')
#       )

# print(longest_trip_distance)


# Ques 8 - Highest Avg fare

# highest_avg_fare = pl_df.select(
#         pl.col('fare_amount').max().alias('highest_avg_fare')
#       )

# print(highest_avg_fare)


#! PANDAS


# Ques 1 - Which Vendor earns more


# most_earning_vendor = (
#     pd_df
#     .groupby("VendorID")["total_amount"]
#     .sum()
#     .reset_index(name="total_earning")
#     .sort_values('total_earning', ascending=False)
#     .head(1)
# )

# print(most_earning_vendor)


# Ques 2 - Highest tip paying payment type


# highest_tip_paying_payment_type = (
#     pd_df
#     .groupby("payment_type")["tip_amount"]
#     .max()
#     .reset_index(name="total_tip")
#     .sort_values('total_tip', ascending=False)
#     .head(1)
# )

# print(highest_tip_paying_payment_type)


# Ques 3 - AVG revenue per trip


# avg_revenue_per_trip = pd_df['total_amount'].mean()

# print(avg_revenue_per_trip)



# Ques 4 - Most common pickup location


# most_common_pu_location = (
#     pd_df
#     .groupby("PULocationID")["PULocationID"]
#     .count()
#     .reset_index(name="total_trips")
#     .sort_values('total_trips', ascending=False)
#     .head(1)
# )

# print(most_common_pu_location)


# Ques 5 - Most common dropoff location


most_common_do_location = (
    pd_df
    .groupby("DOLocationID")["DOLocationID"]
    .count()
    .reset_index(name="total_trips")
    .sort_values('total_trips', ascending=False)
    .head(1)
)

print(most_common_do_location)
