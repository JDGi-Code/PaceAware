# PaceAware Dementia Caregiver Tool

**Description**:  Pacing detection for intervention of dementia-induced wandering behavior. 

  - **Technology stack**: Python
  - **Status**:  Not maintained. 
  - **Platform Proposal Documents and App Handbook**: [Google Docs](https://drive.google.com/drive/folders/1-ZxsGWuHLTMUG1QJrg47m7wvjKXR95TX?usp=drive_link).
    
## Dependencies

Use of this program requires at least one wearable device running the free [Sensor Logger](https://play.google.com/store/apps/details?id=com.kelvin.sensorapp&hl=en_US&gl=US) app. The caregiver should run this program on their own secondary device.

## Installation

## Configuration and Usage

```
python manage.py runserver 8000
```
In wearable device, set up the hot spot. Connect the Caregiver device to the wearable's hot spot. 
Within Sensor Logger app settings on the wearable device, enter Data Streaming, Enable HTTP Push on, Push URL changed to Caregiver device IP address in the following format: 'http://123.123.12.123:8000/data'. The 8000 signifies the port being used by server.py. This can be changed as needed, but must be changed in both places. 
On the caregiver's device, run server.py from this app to start. The app will display 'Detecting...' to show it is running. 

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
