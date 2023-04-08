# NoMoreSQL
Query documents and spreadsheets with natural language
# Demo
![image](https://user-images.githubusercontent.com/40268197/230733615-e850db91-152a-4430-881e-2dbe74aaba5c.png)
# Installation


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

# Usage

Use the `flask run` command and visit 127.0.0.1:5000

# Other notes

Not designed for commercial or production use. This work is very much a proof of concept and has been configured to run on a local server. 

For commercial usage, please refer to the license below & and choose a production-ready WSGI server. Popular options are Gunicorn and uWSGI.

There will be bugs. Although this is an improvement over OpenAI alone, sometimes it gets things wrong. 

Please feel free to contribute by raising an issue or pull request. Unfortunately I can't guarentee the stability or future development plans and the code is provided on an as-is basis with no promises.

# License

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

TL;DR This license lets others distribute, remix, adapt, and build upon this work, even commercially, as long as you credit me for the original creation
