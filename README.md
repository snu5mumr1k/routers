## Description

Development web server for routers' location synchronization inside a big company.
Web server architecture is based on REST.

## Installation

**Use python 3** <br />
**Check `config.py` to get information about models and states**

1. Clone repository
2. Install the required libraries
  1. (optional) [Install virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/). To choose python version: `virtualenv venv -p python3.7`
  2. `python3 -m pip install -r requirements.txt`
3. Setup database (if necessary)
  1. python3 db.py db init
  2. python3 db.py db migrate
  3. python3 db.py db upgrade
4. Start server `python3 run.py`

![Database models](/models.jpg?raw=true)

| HTTP Method | URI                                           | Action                      | Status             | Test               |
| ----------- | --------------------------------------------- | --------------------------- | ------------------ | ------------------ |
| GET         | http://[hostname]/api/routers                 | Retrieve list of routers    | :soon: | :soon: |
| GET         | http://[hostname]/api/routers/[router_id]     | Retrieve a router           | :soon: | :soon: |
| POST        | http://[hostname]/api/routers                 | Create a router             | :soon: | :soon: |
| PUT         | http://[hostname]/api/routers/[router_id]     | Update an existing router   | :soon: | :soon: |
| DELETE      | http://[hostname]/api/routers/[router_id]     | Delete an existing router   | :soon: | :soon: |
||||||
| GET         | http://[hostname]/api/locations               | Retrieve list of locations  | :white_check_mark: | :white_check_mark: |
| GET         | http://[hostname]/api/locations/[location_id] | Retrieve a location         | :white_check_mark: | :white_check_mark: |
| POST        | http://[hostname]/api/locations               | Create a location           | :white_check_mark: | :white_check_mark: |
| PUT         | http://[hostname]/api/locations/[location_id] | Update an existing location | :white_check_mark: | :white_check_mark: |
| DELETE      | http://[hostname]/api/locations/[location_id] | Delete an existing location | :white_check_mark: | :white_check_mark: |
