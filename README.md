# PaceAware Dementia Caregiver Tool

**Description**:  Pacing detection for intervention of dementia-induced wandering behavior. 

  - **Technology stack**: Python
  - **Status**:  Not maintained. 
  - **Platform Proposal Documents and App Handbook**: [Google Docs](https://drive.google.com/drive/folders/1-ZxsGWuHLTMUG1QJrg47m7wvjKXR95TX?usp=drive_link).
    
## Requirements

Use of this program requires at least one wearable device running the free [Sensor Logger](https://play.google.com/store/apps/details?id=com.kelvin.sensorapp&hl=en_US&gl=US) app. The caregiver should run this program on their own secondary device.
Outside libraries used will include:

* colorama: [simple color](https://pypi.org/project/colorama/) for text output (green for not_pacing, yellow for pacing)
* playsound: this [library](https://github.com/TaylorSMarks/playsound) plays a mp3 or wav file.
* alert file download: the [selected file](https://mixkit.co/free-sound-effects/alerts/) has a pleasant sound (unlike a doorbell or an anxiety-inducing alarm) to minimize unintended stress for all parties.
* datetime, json, pandas, flask, and logging libraries

## Files Description
accelmagno_maker.py: Takes a base_filename as a paramter, reads in Accelerometer & Magnetometer csv files, & creates a new df with columns from both sensors, using .round(6) to convert to float32 format.

squisher.py: Combines AccelMagno csv into distinct categories - not_pacing and pacing - which are used as training data.

pacing_detection.py: 

* calc_magnitude(data) & remove_noise(data, sampling_rate)
* extract_features(data, window_sec, sample_rate, activity): reformats time column, resamples & calls add_features on 10 sec windows
* train_tree(frames): performs accuracy test & writes the model to a pickle dump.
* classify_live_window(df): calls all previous functions and reads the pickle.
* test_live_classifier: Read by the server file.

server.py: Reads accelerometer & magnetometer signals from the device.

* classify_live_window: Returns user state, with help from colorama and playsound libraries

## Configuration and Usage

1. In wearable device, set up the hot spot. Connect the Caregiver device to the wearable's hot spot. 
2. Within Sensor Logger app settings on the wearable device, enter Data Streaming, Enable HTTP Push on, Push URL changed to Caregiver device IP address in the following format: 'http://123.123.12.123:8000/data'. The 8000 signifies the port being used by server.py. This can be changed as needed, but must be changed in both places. 
3. On the caregiver's device, run server.py from this app to start. The app will display 'Detecting...' to show it is running.

## Known issues

There are currently no enabled reports capabilities. Reports can be generated from the database directly.

## Getting help

This application is not maintained. Updates by Sensor Logger App may influence the app in unintended ways. Please feel free to create an issue, and maybe someone from the community will support.

## Getting involved

Fork this repo, look through the issues, there is no active developer community at this moment.

----

## Open source licensing info
1. [GPLv3 LICENSE](LICENSE)

----

## Credits and references

1. [Coito, Jack. “Why Seniors with Dementia Pace and Wander.” Legacy Home Care](https://www.legacyhomecare.net/home-care-gold-canyon-az-pacing-and-wander/).
2. [“Dementia.” World Health Organization (WHO), 15 March 2023](https://www.who.int/news-room/fact-sheets/detail/dementia).
3. [Hrisko, Joshua. “Accelerometer, Gyroscope, and Magnetometer Analysis with Raspberry Pi Part I: Basic Readings — Maker Portal.” Maker Portal, 15 November 2019](https://makersportal.com/blog/2019/11/11/raspberry-pi-python-accelerometer-gyroscope-magnetometer).
4. [“Informal Caregivers of People with Dementia: Problems, Needs and Support in the Initial Stage and in Subsequent Stages of Dementia: A Questionnaire Survey.” NCBI, 15 January 2013](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3551235/).
