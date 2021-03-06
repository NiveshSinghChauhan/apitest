# apitest from _Nivesh Singh Chauahan_
apitest for redcarpetup

## prerequisites

+ Python 3
+ pip 3

Postgresql extension prerequisites

- cube
- earthdistance
- postgis

### [API DOCUMENTATION](./APIDocumentation.md)

### Database Setup
create a two table one having name '*mapping*' with having schema:

**key** character varying(10) NOT NULL,<br>
**place_name** character varying(50),<br>
**admin_name1** character varying(50),<br>
**latitude** double precision,<br>
**longitude** double precision,<br>
**accuracy** integer, <br>

and one having name '*maps*' and having schema:

**name** character varying(100) NOT NULL,<br>
**type** character varying(100),<br>
**parent** character varying(100),<br>
**boundry** geometry<br>

after that import *mappings.csv* file in table mapping, And *maps.csv* file in table maps

#### Change the [config.json](./config.json) file according to your database settings.
config option are:

- **DB_NAME** Name of the database eg. _postgres_
- **DB_USER** User of the database eg. _postgres_
- **DB_PASSWORD** Password of the database eg. _password123_
- **HOST** host where the database id hosted eg. _localhost_

### To run this

* pip install -r requirements.txt.
* python [geoapi.py](./geoapi.py)

### To run the tests for this

* python test.py
