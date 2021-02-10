# Cluedo-SE21

Cluedo, Assignment Project, Spring 2021, Software Engineering, UoSussex

## File Structure

```markdown
📦Cluedo-SE21                 - Repository
 ┣ 📂cluedo                     - App Source Folder
 ┃ ┣ 📂resources                  - Binary Resources: Image/Audio...
 ┃ ┣ 📜app.py                     - Application Body
 ┃ ┣ 📜__init__.py                - Package Marker
 ┃ ┗ 📜__main__.py                - Application Entrance
 ┣ 📂data                       - Test or Game Data (not used)
 ┣ 📂docs                       - Documents Folder
 ┃ ┣ 📜changeLog.md               - Do not touch
 ┃ ┗ 📜todo.md                    - Spam ideas here
 ┣ 📂logs                       - Log Files Folder
 ┃ ┗ 📂pytest                     - Log Files of Unit Test
 ┃ ┃ ┣ 📜0210_005235.ptlog          - Date_Time.ptlog
 ┃ ┃ ┗ 📜0210_005334.ptlog
 ┣ 📂tests                      - Unit Test Source Folder
 ┃ ┣ 📜conftest.py                - General test setup
 ┃ ┣ 📜test_app.py                - Test for app.py
 ┃ ┗ 📜__init__.py
 ┣ 📜.gitignore                 - gitignore file
 ┣ 📜LICENSE                    - GNU GPLv3 License
 ┣ 📜Makefile                   - Basic Makefile for convenience
 ┣ 📜pyproject.toml             - Project configuration file
 ┗ 📜README.md                  - Readme
```

## Change Log and Manual(?)

### init, set up *10/02*

- Initialise project repository
- *Hello World*
  - `py -m cluedo` **run app**
- Structure project
- Set up pytest for unit test
  - and logging system
  - `pytest` **run unit test**
- Simple Makefile
  - `nmake run` **run app**
  - `nmake test` **run unit test**
  - `nmake logclear` **clear all empty test logs**
