from peewee import *
import datetime
from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict, dict_to_model
db = PostgresqlDatabase('people', user='victorapaez', password='',
                        host='localhost', port=5432)
class BaseModel(Model):
    class Meta:
        database = db
class Person(BaseModel):
    name = CharField()
    birthday = DateField()
class Pet(BaseModel):
    name = CharField()
    animal_type = CharField()
    person = ForeignKeyField(Person, backref="pets")
db.connect()
db.drop_tables([Pet])
db.drop_tables([Person])
db.create_tables([Person, Pet])
zakk = Person(name='Zakk', birthday=datetime.date(1990, 11, 18))
zakk.save()
victor = Person(name='Vic', birthday=datetime.date(1996, 4, 14))
victor.save()
dog = Pet(name='max', animal_type='dog', person=1)
dog.save()
cat = Pet(name='fur ball', animal_type='cat', person=2)
cat.save()
cat = Pet(name='snow', animal_type='cat', person=1)
cat.save()

app = Flask(__name__)
@app.route('/')
def index():
  return [model_to_dict(pet) for pet in Person.select()]

@app.route('/person/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
  if request.method == 'GET':
    if id:
        return jsonify(model_to_dict(Person.get(Person.id == id)))
    else:
        character_list = []
        for character in Person.select():
            character_list.append(model_to_dict(character))
        return jsonify(character_list)

  if request.method =='PUT':
    body = request.get_json()
    Person.update(body).where(Person.id == id).execute()
    return "Character " + str(id) + " has been updated."

  if request.method == 'POST':
    new_character = dict_to_model(Person, request.get_json())
    new_character.save()
    return jsonify({"success": True})

  if request.method == 'DELETE':
    Person.delete().where(Person.id == id).execute()
    return "Character " + str(id) + " deleted."



app.run(debug=True)