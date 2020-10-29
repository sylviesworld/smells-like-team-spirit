# Note taking app

## Description
An everyday note taking app that supports user profiles and ecrypts all data (files and login information).
Rich text formatting supported to help you take the best, most effective, notes possible.

Happy note taking!

### Group name: smells-like-team-spirit
- [CS-340 Course website](http://web.eecs.utk.edu/courses/fall2020/cosc340/)

## Running the program
From the _smells-like-team-spirit_ directory, run _main.py_:

    UNIX> python main.py
    
There is also a seperate UI being worked on to integrate as the main page in _[app.py](app.py)_. To run it type:

    UNIX> python app.py

## Preview

![Note app screenshot](images/main_screenshot.png)

Icons courtesy of [icons8.com](https://icons8.com/)

## Dependencies 
All dependencies for this project can be found in _[requirements.txt](requirements.txt)_:

```
UNIX> cat requirements.txt
cryptography==3.2.1
PyQt5==5.15.1
bcrypt==3.2.0
```

To automatically install these dependencies, run the following commands in the _smells-like-team-spirit_ directory:

```
UNIX> pip install -r requirements.txt
```

Note: If `certifi` was not installed by running _Install Certificates.command_ when setting up Python, or by doing so manually, install the package before using this program.
- `certifi` documentation:  [link](https://pypi.org/project/certifi/)
- StackOverflow help for Mac, the most common culprit of this issuse: [link](https://stackoverflow.com/questions/42098126/mac-osx-python-ssl-sslerror-ssl-certificate-verify-failed-certificate-verify)

## Known Issues
- Not all buttons are linked/functional in _[app.py](app.py)_

## Authors
[Noah Burgin](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=assignee%3Anoah-22+is%3Aopen),
[Dylan Lomax](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3AMaze-Mind),
[Nick Creech](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3Ancreech1),
[Zach Creech](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3Azach7creech)

