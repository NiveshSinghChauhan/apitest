from flask import Flask, request, json
from math import sin, cos, atan2, radians, sqrt
import psycopg2


app = Flask(__name__)

app.config.from_json('config.json')

connection = psycopg2.connect(dbname=app.config['DB_NAME'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'], host=app.config['HOST'])

# ============================ STAGE 1 ===================================================
@app.route('/post_location', methods=['GET', 'POST'])
def Location():
    cursor = connection.cursor()
    values = {}
    if request.headers['Content-Type'] == 'application/json':
        values = request.get_json(force=True)
    else:
        values = request.form.to_dict(flat=True)
    
    try:
        cursor.execute("SELECT * FROM mapping WHERE key='IN/%s'"% (values['pincode']))
        row = cursor.rowcount

        if not row:
            if 'accuracy' in values:
                query = "INSERT INTO mapping (key, place_name, admin_name1, latitude, longitude, accuracy) \
                VALUES (IN/%s, %s, %s, %s, %s, %s)"% (values['pincode'], values['place_name'], values['admin_name'], values['latitude'], values['longitude'], values['accuracy'])
            else:
                query = "INSERT INTO mapping (key, place_name, admin_name1, latitude, longitude) \
                VALUES ('IN/%s', '%s', '%s', '%s', '%s')"% (values['pincode'], values['address'], values['city'], values['latitude'], values['longitude'])

            cursor.execute(query)
            connection.commit()
            
            return 'New location added.'
        else:
            return 'pincode already exist.'
    except:
        return 'Error, Required Popety are not given'
        


@app.route('/get_location/<string:pincode>')
def GetLocation(pincode):
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM mapping WHERE key='IN/%s'"% (pincode))
    row = cursor.fetchall()

    isexist = cursor.rowcount
    if isexist:

        return json.jsonify({
            'pincode': row[0][0],
            'place_name': row[0][1],
            'city': row[0][2],
            'latitude': row[0][3],
            'longitude': row[0][4]
        })
    else:
        return 'pincode did not exist.'
        

#  =================================== STAGE 2 ====================================

@app.route('/get_using_postgres')
def getUsingPostgres():
    cursor = connection.cursor()

    lat = request.args.to_dict()['latitude']
    lon = request.args.to_dict()['longitude']

    radius = request.args.to_dict()['radius']

    cursor.execute("select * from mapping where earth_box(ll_to_earth(%s, %s), %s) @> ll_to_earth(mapping.latitude, longitude)"% (lat, lon, radius))

    total = cursor.rowcount
    result = cursor.fetchall()

    return json.jsonify({ 'total': total, 'result': result})

@app.route('/get_using_self')
def getUsingSelf():
    cursor = connection.cursor()

    lt = request.args.to_dict()['latitude']
    ln = request.args.to_dict()['longitude']

    radius = request.args.to_dict()['radius']

    cursor.execute("select * from mapping")
    rows = cursor.fetchall()

    R = 6371000
    
    points = []
    for row in rows:
        rlt = row[3]
        rln = row[4]

        # HAVERSINE FORMULA OF CALCULATING OF DISTANCE BETWEEN 2 (LAT/LON)
        lat1 = radians(float(lt))
        lat2 = radians(float(rlt))

        difflat = radians(float(rlt) - float(lt))
        difflon = radians(float(rln) - float(ln))
        
        A = sin( difflat/2 )*sin( difflat/2 ) + cos(lat1)*cos(lat2) * sin( difflon/2 )*sin( difflon/2 )

        c = 2 * atan2(sqrt(A), sqrt((1 - A)))

        dist = R * c

        if dist < float(radius):
            points.append(list(row))

    return json.jsonify({ 'total': points.__len__(), 'result': points})


# =============================== STAGE 3 ==========================
@app.route('/get_place')
def getPlace():
    cursor = connection.cursor()

    lat = request.args.to_dict()['latitude']
    lon = request.args.to_dict()['longitude']

    cursor.execute("SELECT name, type, parent FROM maps m WHERE ST_Covers(m.boundry, ST_Point(%s, %s))"% (lat,lon))

    if cursor.rowcount > 0:
        result = cursor.fetchall()[0]

        return json.jsonify({
                "Place": result[0],
                "Type": result[1],
                "Parent": result[2]
            })
    else:
        return 'Place did not contains the given coordinates.'


if __name__ == '__main__':
    # For Development
    # app.run(debug=True)

    # For Production
    app.run()