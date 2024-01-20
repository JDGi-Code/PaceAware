# Pacing Detection mHealth Application

# This file combines CSVs of various activity types into one CSV
# It was used only during the creation of the labeled data set.

import pandas as pd

# SITTING
#sitting_df = pd.read_csv("data/recording_data/sitting/AccelMagno.csv")
# STANDING
#standing_df = pd.read_csv("data/recording_data/standing/AccelMagno.csv")
# WALKING
#walking_df = pd.read_csv("data/recording_data/walking/AccelMagno.csv")
# PACING
rec_pacing = pd.read_csv("data/recording_data/pacing/AccelMagno.csv")
reg_pacing = pd.read_csv("data/recording_data/AccelMagno.csv")
# concat into one DataFrame
pacing = pd.concat([rec_pacing, reg_pacing], ignore_index=True)
# write new df to file
pacing.to_csv("AccelMagno.csv")