# Pacing Detection mHealth Application

# This is the main python code for the program.
# This file calculates magnitude of accel and magno signals, removes noise, extracts features, and creates the classifier.

import os
import glob
import numpy as np
import pandas as pd
import pickle

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
from scipy.signal import butter, filtfilt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


def calc_magnitude(data):
    data['accel_mag'] = np.sqrt(data['accel_x'] ** 2 + data['accel_y'] ** 2 + data['accel_z'] ** 2)
    data['accel_mag'] -= data['accel_mag'].mean()
    data['magno_mag'] = np.sqrt(data['magno_x'] ** 2 + data['magno_y'] ** 2 + data['magno_z'] ** 2)
    data['magno_mag'] -= data['magno_mag'].mean()
    return data


def remove_noise(data, sampling_rate):
    cutoff = 5
    order = 2
    nyq = sampling_rate * 0.5
    norm_cutoff = cutoff / nyq
    (b, a) = butter(order, norm_cutoff, btype='low')
    data['filtered_accel_mag'] = filtfilt(b, a, data['accel_mag'])
    data['filtered_magno_mag'] = filtfilt(b, a, data['magno_mag'])
    return data


def add_features(window):
    features = {}
    features['a_avg'] = [window['filtered_accel_mag'].mean()]
    features['a_max'] = [window['filtered_accel_mag'].quantile(1)]
    features['a_med'] = [window['filtered_accel_mag'].quantile(0.5)]
    features['a_min'] = [window['filtered_accel_mag'].quantile(0)]
    features['a_q25'] = [window['filtered_accel_mag'].quantile(0.25)]
    features['a_q75'] = [window['filtered_accel_mag'].quantile(0.75)]
    features['a_std'] = [window['filtered_accel_mag'].std()]
    features['m_avg'] = [window['filtered_magno_mag'].mean()]
    features['m_max'] = [window['filtered_magno_mag'].quantile(1)]
    features['m_med'] = [window['filtered_magno_mag'].quantile(0.5)]
    features['m_min'] = [window['filtered_magno_mag'].quantile(0)]
    features['m_q25'] = [window['filtered_magno_mag'].quantile(0.25)]
    features['m_q75'] = [window['filtered_magno_mag'].quantile(0.75)]
    features['m_std'] = [window['filtered_magno_mag'].std()]
    return pd.DataFrame(features)


def extract_features(data, window_sec, sample_rate, activity):
    dfs = []
    data['time'] = pd.to_datetime(data['time'])
    windows = data.set_index('time').resample('{}S'.format(window_sec))
    num_windows = len(windows)
    count = 0
    for (time, window) in windows:
        count += 1
        if count % 1000 == 0:
            print(f'window {count} of {num_windows}')
        features = add_features(window)
        features['activity'] = activity
        dfs.append(features)
    return pd.concat(dfs, ignore_index=True)


def train_tree(frames):
    frames = frames.dropna()
    X = frames[['a_avg', 'a_max', 'a_med', 'a_min', 'a_q25', 'a_q75', 'a_std', 'm_avg', 'm_max', 'm_med', 'm_min', 'm_q25', 'm_q75', 'm_std']]
    y = frames['activity']
    (X_train, X_test, y_train, y_test) = train_test_split(X, y, test_size=0.3, random_state=42)
    dt_model = DecisionTreeClassifier(criterion='entropy', max_depth=5).fit(X_train, y_train)
    dt_pred = dt_model.predict(X_test)
    acc = dt_model.score(X_test, y_test)
    dt_cm = confusion_matrix(y_test, dt_pred, labels=dt_model.classes_)
    print(classification_report(y_test, dt_pred))
    print('Accuracy on test set:', acc)
    print('Accuracy, Rounded to Nearest Hundredth:', acc.round(2))
    return (dt_model, dt_cm, acc)


def create_classifier(all_files):
    dfs = []
    if os.path.isfile('dt_model.pkl'):
        with open('dt_model.pkl', 'rb') as file:
            return (pickle.load(file), None, None)
    for file in all_files:
        sampling_rate = 100
        activity = os.path.basename(os.path.dirname(file))
        data = pd.read_csv(file)
        data = calc_magnitude(data)
        data = remove_noise(data, sampling_rate)
        feature_frames = extract_features(data, 10, sampling_rate, activity)
        dfs.append(feature_frames)
    features_data = pd.concat(dfs, ignore_index=True)
    (dt_model, dt_cm, acc) = train_tree(features_data)
    pickle.dump(dt_model, open('dt_model.pkl', 'wb'))
    return (dt_model, dt_cm, acc)


def classify_live_window(df):
    df = df[df['accel_x'].notna() & df['accel_y'].notna() & df['accel_z'].notna() & df['magno_x'].notna() & df['magno_y'].notna() & df['magno_z'].notna()]
    df = calc_magnitude(df)
    df = remove_noise(df, 100)
    df = add_features(df)
    with open('dt_model.pkl', 'rb') as f:
        model = pickle.load(f)
    y_pred = model.predict(df)
    return y_pred


def test_live_classifier():
    data = {'accel_x': [0.011531], 'accel_y': [0.002931], 'accel_z': [0.019604], 'magno_x': [0.011531], 'magno_y': [0.002931], 'magno_z': [0.019604], 'time': ['2023-08-01 18:40:43.344408']}
    df = pd.DataFrame(data)
    df = pd.concat([df] * 1000, ignore_index=True)
    y_pred = classify_live_window(df)
    print(y_pred)


if __name__ == "__main__":
    # -- MAIN --
    filenames = glob.glob("data/steps_data/**/AccelMagno.csv")
    # create_classifier() saves to pickle
    dt_model, dt_cm, acc = create_classifier(filenames)

    if dt_cm and acc:
        print(acc)
        print(acc.round(2))
