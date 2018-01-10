# project/server/main/views.py
import base64

from flask import render_template, Blueprint, request
from project.server import db
from project.server.models import Auto
from datetime import datetime, timedelta

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.route('/')
def home():
    return render_template('main/home.html')


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")

@main_blueprint.route('/api', methods=['GET', 'POST'])
def add_message():
    content = request.get_json(silent=True)
    for prvek in content['results']:
        prvek['time']=datetime.fromtimestamp(content['epoch_time']/1000)
        image_source = ""
        with open('/var/lib/openalpr/plateimages/%s.jpg'%(content['uuid']),'rb') as f:
            image_source=base64.b64encode(f.read())
        newauto = Auto(**prvek)
        newauto.image = image_source
        db.session.add(newauto)
        db.session.commit()

    return "Ok"
