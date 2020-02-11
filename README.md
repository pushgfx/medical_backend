# medical-backend

### Install Instructions
```console
  $ git clone https://github.com/pushgfx/medical_backend.git
  $ cd medical_backend
  $ virualenv env -p python3

  # OSX/LINUX
  $ source env/bin/activate

  # Windows
  $ env\Scripts\activate

  $ pip install -r requirements.txt


```
### Running The Install
```console
  # OSX/LINUX
  $ export APP_SETTINGS=config.DevelopmentConfig
  $ export FLASK_APP=medical_backend

  # Windows
  $ APP_SETTINGS=config.DevelopmentConfig
  $ set FLASK_APP=hello

  $ flask run



