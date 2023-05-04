from autostereogram import make_stereogram
import os
from flask import Flask, render_template, abort, request, jsonify, send_from_directory, Response, redirect
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy import Column, Integer, DateTime
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
from base64 import b64encode
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Stereo(db.Model):
    __tablename__ = 'stereo'
    id = Column(Integer, primary_key=True)
    image = db.Column(BLOB)
    date = db.Column(DateTime(timezone=True), server_default=func.now())

migrate = Migrate(app, db)

cors = CORS(app, resources={r"*": {"origins": "*"}})

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route('/')
def index():
    image_id = request.args.get('img')
    dir_path = os.path.join(basedir, 'static/img/pattern')
    res = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            if path != '.DS_Store':
                res.append(path)
    if image_id:
        return render_template('result.html', image_id=image_id)
    return render_template('index.html', pttrns=res)


app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'),404
 
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'),500

@app.route('/generate', methods=["POST",])
def generate():
    input_image = request.files.get("image")
    pattern = request.form.get('pattern')
    output_image = make_stereogram(input_image, pattern)
    stereo = Stereo(image = output_image)
    db.session.add(stereo)
    db.session.commit()
    image_id = stereo.id
    return redirect('/?img='+str(image_id))

@app.route('/img', methods=['GET',])
def image():
    img = request.args.get('img_id')
    stereo = db.session.query(Stereo).get(img)
    if stereo.image:
        return Response(stereo.image, mimetype="image/png")
    else:
        abort(400) 


@app.route('/list-batik')
def tentang_batik():
    res = []
    dir_path = os.path.join(basedir, 'static/img/pattern')
    tmp_path = os.path.join(basedir, 'templates/batik')
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            if path != '.DS_Store':
                res.append(path)
    content = {}
    for rs in res:
        nme = rs.replace('.png', '').replace('.jpg','')
        try:
            fle = open(os.path.join(tmp_path, nme+'.html'), 'r').read()
        except:
            fle = ""
        content[rs] = fle
    return render_template('tentang-batik.html', tentang=content)

if __name__ == '__main__':
   app.run(debug = True)