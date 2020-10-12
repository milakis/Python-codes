# Python-codes
Codes for work

###Setup:

In terminal, go to the source of the project
```
cd /path/to/project/Python-codes
```

Create virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip install --upgrade pip
pip install google-cloud-vision opencv-python pillow pandas openpyxl
```

Get your Google Cloud API credentials: https://cloud.google.com/vision/docs/libraries#setting_up_authentication

Set the environment variable
```
export GOOGLE_APPLICATION_CREDENTIALS="[PATH]"
```