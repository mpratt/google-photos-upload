# Google Photos Upload
Python script used to upload pictures to Google Photos.
It uploads the media and organizes the data in albums using the name
of the folder containing the data.

This script requires that you create Google Cloud Project and generate Oauth credentials.
You can start the process by going to [Google Cloud Project](https://console.cloud.google.com/)

# Installation
Download the source code, extract the data, go to the folder and run

`pip install -e .`

# Usage
```
google-photos-upload folder_with_media --credentials /path/to/credentials.json
```
