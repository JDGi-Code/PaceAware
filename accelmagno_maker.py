# Pacing Detection mHealth Application

# This file combines Accelerometer and Magnetometer CSVs into one file called AccelMagno.csv.
# It was used only during the creation of the labeled data set.

import pandas as pd

basename = "data/recording_data"
#sitting_basename = basename + "/sitting"
#standing_basename = basename + "/standing"
#walking_basename = basename + "/walking"
pacing_basename = basename + "/pacing"

# sitting_accel_filename = sitting_basename + "/Accelerometer.csv"
# standing_accel_filename = standing_basename + "/Accelerometer.csv"
# walking_accel_filename = walking_basename + "/Accelerometer.csv"
#
# sitting_magno_filename = sitting_basename + "/Magnetometer.csv"
# standing_magno_filename = standing_basename + "/Magnetometer.csv"
# walking_magno_filename = walking_basename + "/Magnetometer.csv"

def processor(base_filename):
    accel_df = pd.read_csv(base_filename + "/Accelerometer.csv")
    accel_df['time'] = pd.to_datetime(accel_df['time'], unit='ns')

    magno_df = pd.read_csv(base_filename + "/Magnetometer.csv")
    magno_df['time'] = pd.to_datetime(magno_df['time'], unit='ns')

    new_df = pd.DataFrame(columns=["time","accel_x","accel_y","accel_z","magno_x","magno_y","magno_z"])
    new_df['time'] = accel_df['time']
    new_df['accel_x'] = accel_df['x'].round(6)
    new_df['accel_y'] = accel_df['y'].round(6)
    new_df['accel_z'] = accel_df['z'].round(6)
    new_df['magno_x'] = magno_df['x'].round(6)
    new_df['magno_y'] = magno_df['y'].round(6)
    new_df['magno_z'] = magno_df['z'].round(6)

    new_df.to_csv(base_filename + "/AccelMagno.csv", index=False)


#processor(sitting_basename)
#processor(standing_basename)
#processor(walking_basename)
processor(pacing_basename)