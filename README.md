# Maintenance Assistant
System to provide Asset Management for maintenance managers. More information is available in the Wiki.

## Getting Started
### Prerequisites
* Python 3.12.x

### Installation
1. Install Python 3.12.2
2. Clone the repo:
<br> `git clone https://github.com/Str-Josh/MaintenanceAssistant.git`
<br> `cd MaintenanceAssistant`
4. Change git remote url to avoid accidental pushes to main project
<br>`git remote set-url origin github_username/repo_name`
<br>`git remote -v`
5. Initialize and activate a virtual environment:
<br> `python -m venv env`
<br> `source env/bin/activate`
7. Install dependencies:
<br>`pip install -r requirements.txt`
8. Run development server:
<br> `python app.py`
9. Goto http://localhost:5000


### File Structure
--------

  ```sh
    ├── README.md
    ├── app.py
    ├── config.py
    ├── database.db
    ├── errors.log
    ├── mymodels.py
    ├── requirements.txt
    ├── utils.py
    ├── static
    │   ├── pages
    │   │   ├── stylesheet.css
    │   ├── layouts
    │   │   ├── nav.css
    │   │   └── navbar_styles.css
    │   ├── img
    │       ├── Logout.png
    │       ├── alert.png
    │       ├── logo.png
    │       ├── mail.png
    │       ├── search.png
    │       └── time.png
    └── templates
        ├── index.html
        ├── user_profile.html
        ├── errors
        │   ├── 404.html
        │   ├── unauth.html
        │   └── 500.html
        ├── forms
        │   ├── forgot.html
        │   └── sign_up.html
        ├── layouts
        │   ├── nav.html
        │   └── navbar.html
        ├── pages
        │   ├── DepartmentHome.html
        │   ├── devicedetail.html
        │   ├── reportbreak.html
        │   ├── sendrequest.html
        │   ├── updateusage.html
        │   └── viewdevices.html
        └── tests
            └── main.html
  ```

## Project Outcomes
### Future Additions/Improvements:
* ...
