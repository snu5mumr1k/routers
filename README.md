# About [![Build Status](https://travis-ci.com/snu5mumr1k/routers.svg?branch=master)](https://travis-ci.com/snu5mumr1k/routers)

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
5. For contributors:
  1. To run tests use `python3 -m pytest` (https://docs.pytest.org/en/latest/)
  2. Do not forget to run style checks: `python3 -m flake8` (http://flake8.pycqa.org/en/latest/)

![Database models](/models.jpg?raw=true)

|                         | HTTP Method | URI                                           | Action                      | Status             | Test               |
| ----------------------- | ----------- | --------------------------------------------- | --------------------------- | ------------------ | ------------------ |
| [DOC](#get_routers)     | GET         | http://[hostname]/api/routers                 | Retrieve list of routers    | :white_check_mark: | :white_check_mark: |
| [DOC](#get_router)      | GET         | http://[hostname]/api/routers/[router_id]     | Retrieve a router           | :white_check_mark: | :white_check_mark: |
| [DOC](#create_router)   | POST        | http://[hostname]/api/routers                 | Create a router             | :white_check_mark: | :white_check_mark: |
| [DOC](#update_router)   | PUT         | http://[hostname]/api/routers/[router_id]     | Update an existing router   | :white_check_mark: | :white_check_mark: |
| [DOC](#delete_router)   | DELETE      | http://[hostname]/api/routers/[router_id]     | Delete an existing router   | :white_check_mark: | :white_check_mark: |
|||||||
| [DOC](#get_locations)   | GET         | http://[hostname]/api/locations               | Retrieve list of locations  | :white_check_mark: | :white_check_mark: |
| [DOC](#get_location)    | GET         | http://[hostname]/api/locations/[location_id] | Retrieve a location         | :white_check_mark: | :white_check_mark: |
| [DOC](#create_location) | POST        | http://[hostname]/api/locations               | Create a location           | :white_check_mark: | :white_check_mark: |
| [DOC](#update_location) | PUT         | http://[hostname]/api/locations/[location_id] | Update an existing location | :white_check_mark: | :white_check_mark: |
| [DOC](#delete_location) | DELETE      | http://[hostname]/api/locations/[location_id] | Delete an existing location | :white_check_mark: | :white_check_mark: |

<a name="get_routers"></a>
**Get routers**
----
  Returns json data about all routers.

* **URL**

  /api/routers

* **Method:**

  `GET`

* **URL Params**

  **Optional:**

  `offset=[integer]`
  `limit=[integer]`
  `model=[string]`
  `state=[string]`
  `location_id=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"routers": [{"id": 2, "time_updated": "2016-05-23 22:05:04", "location_id": 1, "time_created": "2016-05-23 22:05:04", "model": "ASUS", "state": "deactivated"}, {"id": 1, "time_updated": "2016-05-23 22:05:03", "location_id": 1, "time_created": "2016-05-23 22:05:03", "model": "ASUS", "state": "deactivated"}]}`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Limit is not integer"}`

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Offset is not integer"}`

<a name="get_router"></a>
**Get one router**
----
  Returns json data about a single router.

* **URL**

  /api/routers/:id

* **Method:**

  `GET`

* **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"router": {"id": 1, "model": "ASUS", "time_updated": "2016-05-23 22:05:03", "time_created": "2016-05-23 22:05:03", "state": "deactivated", "location_id": 1}}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "Router not found"}`

<a name="create_router"></a>
**Create new router**
----
  Returns json data about new router. Location header keeps new item's URI.

* **URL**

  /api/routers

* **Method:**

  `POST`

* **URL Params**

  None

* **Data Params**

  **Required:**

  `model=[string]`

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{"router": {"id": 4, "model": "ASUS", "time_updated": "2016-05-23 22:20:38", "time_created": "2016-05-23 22:20:38", "state": "deactivated", "location_id": 1}}`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should be json"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should contain model"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should be json"}`

<a name="update_router"></a>
**Update router**
----
  Returns json data about updated router.

* **URL**

  /api/routers/:id

* **Method:**

  `PUT`

* **URL Params**

  None

* **Data Params**

  **Optional:**

  `model=[string]`
  `state=[string]`
  `location_id=[integer]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"router": {"id": 4, "model": "ASUS", "time_updated": "2016-05-23 22:20:38", "time_created": "2016-05-23 22:20:38", "state": "deactivated", "location_id": 1}}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "Router not found"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should be json"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Model is not supported"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "State is not supported"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Location id should be integer"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Location does not exist"}`

<a name="delete_router"></a>
**Delete router**
----
  Returns empty body.

* **URL**

  /api/routers/:id

* **Method:**

  `DELETE`

* **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 204

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "Router not found"}`

<a name="get_locations"></a>
**Get locations**
----
  Returns json data about all locations.

* **URL**

  /api/locations

* **Method:**

  `GET`

* **URL Params**

  **Optional:**

  `offset=[integer]`
  `limit=[integer]`

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"locations": [{"routers": [{"id": 1, "model": "AirTight", "time_updated": "2016-05-23 22:28:33", "time_created": "2016-05-23 22:05:03", "state": "activated", "location_id": 2}], "id": 2, "address": "Moscow", "time_created": "2016-05-23 21:18:02", "time_updated": "2016-05-23 21:18:02"}]}`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Limit is not integer"}`

  OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Offset is not integer"}`

<a name="get_location"></a>
**Get one location**
----
  Returns json data about a single location.

* **URL**

  /api/locations/:id

* **Method:**

  `GET`

* **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"location": {"routers": [{"id": 1, "model": "AirTight", "time_updated": "2016-05-23 22:28:33", "time_created": "2016-05-23 22:05:03", "state": "activated", "location_id": 2}], "id": 2, "address": "Moscow", "time_created": "2016-05-23 21:18:02", "time_updated": "2016-05-23 21:18:02"}}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "Location not found"}`

<a name="create_location"></a>
**Create new location**
----
  Returns json data about new location. Location header keeps new item's URI.

* **URL**

  /api/locations

* **Method:**

  `POST`

* **URL Params**

  None

* **Data Params**

  **Required:**

  `address=[string]`

* **Success Response:**

  * **Code:** 201 <br />
    **Content:** `{"location": {"routers": [], "id": 3, "address": "ASUS", "time_created": "2016-05-23 22:35:36", "time_updated": "2016-05-23 22:35:36"}}`

* **Error Response:**

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should be json"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should contain address"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should be json"}`

<a name="update_location"></a>
**Update location**
----
  Returns json data about updated router.

* **URL**

  /api/locations/:id

* **Method:**

  `PUT`

* **URL Params**

  None

* **Data Params**

  **Optional:**

  `address=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"location": {"routers": [], "id": 3, "address": "USA", "time_created": "2016-05-23 22:35:36", "time_updated": "2016-05-23 22:36:54"}}`

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "Location not found"}`

    OR

  * **Code:** 400 BAD REQUEST <br />
    **Content:** `{"error": "Request should be json"}`

<a name="delete_location"></a>
**Delete location**
----
  Returns empty body.

* **URL**

  /api/locations/:id

* **Method:**

  `DELETE`

* **URL Params**

  None

* **Data Params**

  None

* **Success Response:**

  * **Code:** 204

* **Error Response:**

  * **Code:** 404 NOT FOUND <br />
    **Content:** `{"error": "Location not found"}`
