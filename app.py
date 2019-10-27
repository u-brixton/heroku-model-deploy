import os
import json
import pickle
from sklearn.externals import joblib
import pandas as pd
from flask import Flask, jsonify, request
import psycopg2
from peewee import (
    SqliteDatabase, PostgresqlDatabase, Model, IntegerField,
    FloatField, TextField, IntegrityError
)
from playhouse.shortcuts import model_to_dict

DATABASE_URL2 =  "postgres://axjyqoghnzvcvs:7fbb5d724a69284482896f914629796976e27258acf09bcdc9aedbf6081b64cf@ec2-46-137-113-157.eu-west-1.compute.amazonaws.com:5432/d5av4o4gbmrpqi"
conn = psycopg2.connect(DATABASE_URL2, sslmode='require')    
cur = conn.cursor()



########################################
# Begin database stuff

if 'DATABASE_URL' in os.environ:
    db_url = os.environ['DATABASE_URL']
    dbname = db_url.split('@')[1].split('/')[1]
    user = db_url.split('@')[0].split(':')[1].lstrip('//')
    password = db_url.split('@')[0].split(':')[2]
    host = db_url.split('@')[1].split('/')[0].split(':')[0]
    port = db_url.split('@')[1].split('/')[0].split(':')[1]
    DB = PostgresqlDatabase(
        dbname,
        user=user,
        password=password,
        host=host,
        port=port,
    )
else:
    DB = SqliteDatabase('predictions.db')


class answers_short(Model):
    item = IntegerField()
    student=IntegerField()
   # response_time=IntegerField()
   # correct=IntegerField()
    #difficulty=FloatField()
    #student_elo=FloatField()
    #item_elo=FloatField()
    #prob=FloatField()

    class Meta:
        database = DB

DB.create_tables([answers_short], safe=True)


# End database stuff
########################################

########################################
# Unpickle the previously-trained model


with open('columns.json') as fh:
    columns = json.load(fh)

pipeline = joblib.load('pipeline.pickle')

with open('dtypes.pickle', 'rb') as fh:
    dtypes = pickle.load(fh)


# End model un-pickling
########################################


########################################
# Begin webserver stuff

app = Flask(__name__)

@app.route('/print_table',methods=["POST"])
def print_table():
    cur.execute("SELECT * FROM answers_short")
    a=cur.fetchall()
    return a

# End webserver stuff
########################################

if __name__ == "__main__":
    app.run(debug=True, port=5000)