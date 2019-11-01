import sqlalchemy as db
import json
import datetime as dt
import requests
import xml.etree.ElementTree as ET
import sys
from sqlalchemy.dialects.postgresql import insert

def lambda_handler(event,context):

    prestring = "{http://www.ecb.int/vocabulary/2002-08-01/eurofxref}" #the xml-file uses this as a namespace, therefore we have to put this string in front of the tag
    ecb_xml_adress = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml?3320341163d47cb6f9f32b132f30a4cc" #Link to the ecb file for the exchange rates of the last 20 days

    num_days = 10 #number of days we want to load into the database

    def get_xml(adress):
        try:
            response =  requests.get(adress)

            if not (response.status_code == 200):
                return "Error: response {}".format(response)
            return response
        except  requests.exceptions.RequestException as error:
            return "Error {0}".format(error)

    response = get_xml(ecb_xml_adress)
    xml = ET.fromstring(response.content)

    values = []
    counter = 0

    for r in xml.find(prestring+'Cube'):
        if ("time" in r.attrib) and (counter< num_days):
            date = dt.datetime.strptime(r.attrib["time"],'%Y-%m-%d').date()
            datum = r.attrib['time']
            counter+=1
            for k in r.getchildren():
                curr = k.attrib['currency']
                rate = k.attrib['rate']
                values.append((date,curr,rate))

    engine = db.create_engine('postgresql://naphets:postgres_dev@database-ecb.cxkslz20bb7r.eu-central-1.rds.amazonaws.com:5432/postgres')


    connection = engine.connect()

    metadata = db.MetaData()


    exchange = db.Table('exchange_rates',metadata, autoload=True, autoload_with=engine)



    query = insert(exchange).values(values)
    query = query.on_conflict_do_nothing()
    engine.execute(query)

    return {
        	'statusCode': 200,
        	'body': json.dumps('Hello from Lambda!')
	    }
