from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum, to_timestamp, collect_list, struct
import os

# Start Spark session
spark = SparkSession.builder.appName("DriverBehaviorSummary").getOrCreate()

# Read all raw lines
lines = spark.read.text("/home/archun/Desktop/comp4443/data/*.csv").rdd.map(lambda r: r[0])

# Fix row lengths
def fix_row_length(fields):
    if len(fields) < 19:
        return fields + [''] * (19 - len(fields))
    elif len(fields) > 19:
        return fields[:19]
    else:
        return fields

rows = lines.map(lambda line: line.split(',')).map(fix_row_length)

# Convert to DataFrame
df = rows.toDF([
    "driverID", "carPlateNumber", "Latitude", "Longitude", "Speed", "Direction",
    "siteName", "Time", "isRapidlySpeedup", "isRapidlySlowdown", "isNeutralSlide",
    "isNeutralSlideFinished", "neutralSlideTime", "isOverspeed", "isOverspeedFinished",
    "overspeedTime", "isFatigueDriving", "isHthrottleStop", "isOilLeak"
])

# Cast important columns
df = df.withColumn("isOverspeed", col("isOverspeed").cast("int")) \
       .withColumn("overspeedTime", col("overspeedTime").cast("int")) \
       .withColumn("isFatigueDriving", col("isFatigueDriving").cast("int")) \
       .withColumn("neutralSlideTime", col("neutralSlideTime").cast("int")) \
       .withColumn("Speed", col("Speed").cast("int")) \
       .withColumn("Time", to_timestamp("Time"))

# === A. Summary Table (already working) ===
summary = df.groupBy("carPlateNumber").agg(
    _sum("isOverspeed").alias("overspeed_count"),
    _sum("overspeedTime").alias("total_overspeed_time"),
    _sum("isFatigueDriving").alias("fatigue_count"),
    _sum("neutralSlideTime").alias("total_neutral_slide_time")
)

summary_output_path = "/home/archun/Desktop/comp4443/results/summary.json"
summary.toPandas().to_json(summary_output_path, orient="records")

# === B. Speed Time Series per Driver ===
speed_df = df.select("carPlateNumber", "Time", "Speed").where(col("Speed").isNotNull())

speed_grouped = speed_df.groupBy("carPlateNumber").agg(
    collect_list(struct(col("Time").alias("timestamp"), col("Speed"))).alias("records")
)

speed_output_path = "/home/archun/Desktop/comp4443/results/speed_data.json"
speed_grouped.toPandas().to_json(speed_output_path, orient="records", date_format="iso")

# Stop Spark
spark.stop()

print("✅ Summary and speed data saved.")
