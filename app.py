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


# class Prediction(Model):
#     observation_id = IntegerField(unique=True)
#     observation = TextField()
#     proba = FloatField()
#     true_class = IntegerField(null=True)

#     class Meta:
#         database = DB

DB.create_tables([Prediction], safe=True)


class Prediction(Model):
    item = IntegerField()
    student=IntegerField()
    #response_time=IntegerField()
    #correct=IntegerField()
    #difficulty=FloatField()
    #student_elo=FloatField()
    #item_elo=FloatField()
    #prob=FloatField()

    class Meta:
        database = DB

DB.create_tables([Prediction], safe=True)
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

@app.route('/list-db-contents')
def list_db_contents():
    return jsonify([
        model_to_dict(obs) for obs in Prediction.select()
    ])


# End webserver stuff
########################################

if __name__ == "__main__":
    app.run(debug=True, port=5000)