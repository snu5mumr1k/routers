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
3. Start server `python3 run.py`

![Database models](/models.jpg?raw=true)

| HTTP Method | URI                                           | Action                      | Status             | Test               |
| ----------- | --------------------------------------------- | --------------------------- | ------------------ | ------------------ |
| GET         | http://[hostname]/api/routers                 | Retrieve list of routers    | :soon: | :soon: |
| GET         | http://[hostname]/api/routers/[router_id]     | Retrieve a router           | :soon: | :soon: |
| POST        | http://[hostname]/api/routers                 | Create a router             | :soon: | :soon: |
| PUT         | http://[hostname]/api/routers/[router_id]     | Update an existing router   | :soon: | :soon: |
| DELETE      | http://[hostname]/api/routers/[router_id]     | Delete an existing router   | :soon: | :soon: |
||||||
| GET         | http://[hostname]/api/locations               | Retrieve list of locations  | :soon: | :soon: |
| GET         | http://[hostname]/api/locations/[location_id] | Retrieve a location         | :soon: | :soon: |
| POST        | http://[hostname]/api/locations               | Create a location           | :soon: | :soon: |
| PUT         | http://[hostname]/api/locations/[location_id] | Update an existing location | :soon: | :soon: |
| DELETE      | http://[hostname]/api/locations/[location_id] | Delete an existing location | :soon: | :soon: |
