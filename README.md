# Cluedo-SE21

Cluedo, Assignment Project, Spring 2021, Software Engineering, UoSussex

## File Structure

```markdown
📦Cluedo-SE21                 - Repository
 ┣ 📂cluedo                     - App Source Folder
 ┃ ┣ 📂cmd                        - Backend command line util (not full game)
 ┃ ┃ ┣ 📂data                       - Game Data
 ┃ ┃ ┃ ┗ 📜default.json               - Default Game Setup
 ┃ ┃ ┗ 📜xxx.py                     - Code for command line util
 ┃ ┣ 📂images                     - Binary Resources: Image
 ┃ ┣ 📜ingame.py                  - App GUI controller
 ┃ ┣ 📜ingame.ky                  - App GUI layout sheet
 ┃ ┣ 📜__init__.py                - Package Marker
 ┃ ┗ 📜__main__.py                - Application Entrance
 ┣ 📂dev                        - More complete command line version game
 ┣ 📂logs                       - Log Files Folder
 ┃ ┗ 📂pytest                     - Log Files of Unit Test
 ┃ ┃ ┣ 📜0210_005235.ptlog          - Date_Time.ptlog
 ┃ ┃ ┗ 📜0210_005334.ptlog
 ┣ 📂tests                      - Unit Test Source Folder
 ┃ ┣ 📜conftest.py                - General test setup
 ┃ ┣ 📜test_xxx.py                - Test for xxx.py
 ┃ ┗ 📜__init__.py
 ┣ 📜.gitignore                 - gitignore file
 ┣ 📜LICENSE                    - GNU GPLv3 License
 ┣ 📜Makefile                   - Basic Makefile for convenience
 ┣ 📜pyproject.toml             - Project configuration file
 ┗ 📜README.md                  - Readme
```

## Manual

Need to install Kivy to run app

- `py -m cluedo` **run app**
- `pytest` **run unit test**
- `nmake run` **run app**
- `nmake test` **run unit test**
- `nmake logclear` **clear all empty test logs**
