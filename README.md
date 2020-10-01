# Note taking app
### Group name: smells-like-team-spirit
- [CS-340 Course website](http://web.eecs.utk.edu/courses/fall2020/cosc340/)

## Running the program
From the _smells-like-team-spirit_ directory, run _main.py_:

    UNIX> python main.py
    
There is also a seperate UI being worked on to integrate as the main page in _[app.py](app.py)_. To run it type:

    UNIX> python app.py

## Dependencies 
All dependencies for this project can be found in _[requirements.txt](requirements.txt)_:

```
UNIX> cat requirements.txt
PyQt5==5.15.1
```

To automatically install these dependencies, run the following commands in the _smells-like-team-spirit_ directory:

```
UNIX> pip install -r requirements.txt
```

## Known Issues
- Creating an account with an invalid email will crash the program
- Not all buttons are linked/functional in _[app.py](app.py)_
- Icon sizes in toolbar differ between Windows and MacOS, creating small buttons on Windows (normal on Mac)


## Authors
[Noah Burgin](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=assignee%3Anoah-22+is%3Aopen),
[Dylan Lomax](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3AMaze-Mind),
[Nick Creech](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3Ancreech1),
[Zach Creech](https://github.com/UTK-CS340-Fall-2020/smells-like-team-spirit/issues?q=is%3Aopen+assignee%3Azach7creech)
