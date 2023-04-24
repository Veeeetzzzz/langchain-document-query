# NoMoreSQL
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

Proof of concept that let's you query documents, spreadsheets and databases with natural language
# Demo
![image](https://user-images.githubusercontent.com/40268197/233853273-94d1c117-dce0-4be5-9698-db9ff3d3408e.png)
# Installation for Windows


Python - https://www.python.org/downloads/

If you've used `git clone` before skip, if not run in PowerShell:

`winget install --id Git.Git -e --source winget`

Then clone:

`git clone https://github.com/Veeeetzzzz/NoMoreSQL.git`

Change directory:

`cd NoMoreSQL`

Install requirements: 

`pip install -r requirements.txt`

Bring your own OpenAI API key - set it as an enviroment variable called `OPEN_API_KEY`

# Installation for Linux

Python - Install Python from your package manager or by visiting https://www.python.org/downloads/

If you've used git clone before, skip this. If not, install git by running in Terminal:

`sudo apt-get update`
`sudo apt-get install git`

For other Linux distributions, use the appropriate package manager and command.

Then clone the repository:

`git clone https://github.com/Veeeetzzzz/NoMoreSQL.git`

Change directory:

`cd NoMoreSQL`

Install requirements:

`pip install -r requirements.txt`

Bring your own OpenAI API key - set it as an environment variable called OPEN_API_KEY:

`export OPEN_API_KEY="your_openai_api_key_here"`

Replace 'your_openai_api_key_here' with your actual OpenAI API key.

# Usage

Use the `flask run` command and visit 127.0.0.1:5000

# Enhancments

Feel free to submit a PR if you'd like to contribute to this repo - to do list:

Adding client-side validation: The current code only checks if the required fields are not empty, but it would be better to perform more validation on the input files, such as their size or ensuring that they are in the correct format.

Handling server-side errors: The current code only displays an error message if there is an error with the POST request. It would be better to handle any errors returned by the server and display them to the user instead of just showing a generic error message.

Providing feedback to the user during file upload: Currently, the user does not receive any feedback while their files are being uploaded. It would be useful to provide a progress bar or some other feedback mechanism to let the user know that the process is ongoing.

# Other notes

Not designed for commercial or production use. This work is very much a proof of concept and has been configured to run on a local server. 

For commercial usage, please refer to the license below & and choose a production-ready WSGI server. Popular options are Gunicorn and uWSGI.

There will be bugs. Although this is an improvement over OpenAI alone, sometimes it gets things wrong. 

Please feel free to contribute by raising an issue or pull request. Unfortunately I can't guarentee the stability or future development plans and the code is provided on an as-is basis with no promises.
