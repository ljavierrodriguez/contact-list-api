from flask import Flask, render_template, request, jsonify
from flask import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db, Contact

app = Flask(__name__)

app.url_map.strict_slashes = False

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://<user>:<passwd>@<ip_servidor>:<port>/<database_name>'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://lrodriguez:derek.15@localhost:3306/contactlist'

db.init_app(app)
Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand) #  init migrate upgrade downgrade

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/apis/fake/contact/agenda', methods=['GET'])
def all_agendas():
    '''
    agendas = Contact.query.all()
    agendas = set(map(lambda contact: contact.agenda_slug, agendas))
    unique_agendas = []
    for agenda in agendas:
        unique_agendas.append(agenda)
    return jsonify(unique_agendas), 200
    '''
    agendas = Contact.query.with_entities(Contact.agenda_slug).distinct()
    agendas = list(map(lambda contact: contact.agenda_slug, agendas))
    return jsonify(agendas), 200

@app.route('/apis/fake/contact/agenda/<agenda_slug>', methods=['GET', 'DELETE'])
def all_contacts_by_agenda(agenda_slug):
    if request.method == 'GET':
        contacts = Contact.query.filter_by(agenda_slug=agenda_slug).all()
        contacts = list(map(lambda contact: contact.serialize(), contacts))
        return jsonify(contacts), 200

    if request.method == 'DELETE':
        contacts = Contact.query.filter_by(agenda_slug=agenda_slug).all()
        for contact in contacts:
            if contact:
                contact.delete()
        return jsonify({"success": "All contacts deleted"}), 200

@app.route('/apis/fake/contact/<int:contact_id>', methods=['GET', 'PUT', 'DELETE'])
def contact(contact_id):
    if request.method == 'GET':
        pass
    if request.method == 'PUT':
        pass
    if request.method == 'DELETE':
        pass

@app.route('/apis/fake/contact', methods=['POST'])
def create_contact():
    full_name = request.json.get("full_name", None)
    email = request.json.get("email", None)
    agenda_slug = request.json.get("agenda_slug", None)
    address = request.json.get("address", "")
    phone = request.json.get("phone", "")

    if not full_name:
        return jsonify({"msg": "full_name is required"}), 400

    contact = Contact()
    contact.full_name = full_name
    contact.email = email
    contact.agenda_slug = agenda_slug
    contact.address = address
    contact.phone = phone

    contact.save()

    return jsonify(contact.serialize()), 201


if __name__ == '__main__':
    manager.run()