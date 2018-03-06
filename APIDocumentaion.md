# API DOCUMENTAION
##### STAGE 1
---------------------------------------------------------------------------------------------------------------------------------
### POST '/post_location'

To Add new Location to the databse.


__'Content-Type: application/json'__
#### porperty required in the body of post is :

**pincode**- pincode of the place<br>
**address** - address of the place<br>
**city** - city the place is in <br>
**latitude** - latitude of the place<br>
**longitude** - longitude of the place<br>

### GET '/get_location/<*PINCODE*>'

To Get the location of the given pincode
replace the *PINCODE* with the pincode of the place.

##### STAGE 2
---------------------------------------------------------------------------------------------------------------------------------
### GET '/get_using_postgres'

To get the pincode in the given radius around the a give coordinates(lat/lon)

#### Query parmas required is :

**radius** - radius to get pincodes around the a coordinates <br>
**latitude** - latitude of the point around which to get the pincodes <br>
**longitude** - longitude of the point around which to get the pincodes <br>

### GET '/get_using_self'

To get the pincode in the given radius around the a give coordinates(lat/lon) using the self calculated radius.

#### Query parmas required is :

**radius** - radius to get pincodes around the a coordinates <br>
**latitude** - latitude of the point around which to get the pincodes <br>
**longitude** - longitude of the point around which to get the pincodes <br>

##### STAGE 3
---------------------------------------------------------------------------------------------------------------------------------
### GET '/get_place'

To get the place in which the given coordinates(lat/lon) lies in.

#### Query parmas required is :

**latitude** - latitude of the point around which to get the pincodes <br>
**longitude** - longitude of the point around which to get the pincodes <br> 