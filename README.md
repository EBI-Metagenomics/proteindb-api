# MGnify Protein DB - API

This is a first draft of an RESTful API built on top of the MGnify Protein DB.

## Setup

User a conda or a python virtual env.

```bash
$ pip install -r requirements-dev.txt
```

### Execution

Set the mysql connection details in a `.env` file in the app folder, the content should be:

```
MYSQL_HOST=
MYSQL_PORT=
MYSQL_DB=
MYSQL_USER=
MYSQL_PASS=
```

To run the dev server:

```bash
$ uvicorn api.main:app --reload 
```