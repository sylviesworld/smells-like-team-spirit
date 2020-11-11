# Note taking app

## Description
An everyday note taking app that supports user profiles and ecrypts all data (files and login information).
Rich text formatting supported to help you take the best, most effective, notes possible.

Happy note taking!

### Group name: smells-like-team-spirit
- [CS-340 Course website](http://web.eecs.utk.edu/courses/fall2020/cosc340/)


## Running the program
From the _smells-like-team-spirit_ directory, run _[main.py](app.py)_:

    UNIX> python main.py
    
There is also a seperate UI that implements the same core features (rich text, accounts, data encryption) as _main.py_ with a different interface. It is developed with multitasking in mind, supporting 2 note tabs at once and has the file open and save options pinned to the side of the window, allowing users to quickly switch between notes. Run this version with _[app.py](app.py)_:

    UNIX> python app.py


## Preview

![Note app screenshot](images/main_screenshot.png)

Toolbar icons sourced from the Blue UI set at [icons8.com](https://icons8.com/).


## Dependencies 
All dependencies for this project are listed in _[requirements.txt](requirements.txt)_:

```
UNIX> cat requirements.txt
cryptography
PyQt5
bcrypt
certifi
```

To automatically install these dependencies, run the following commands in the _smells-like-team-spirit_ directory:

```
UNIX> pip install -r requirements.txt
```


## Authors
[Noah Burgin](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=assignee%3Anoah-22+is%3Aopen),
[Dylan Lomax](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3AMaze-Mind),
[Nick Creech](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3Ancreech1),
[Zach Creech](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3Azach7creech)

