import sys
import yaml
import json
#sys.path.append('./source')
from source.neo import Neo
import os
from flask import Flask, render_template, request
import datetime as dt

with open(r'../config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
m = Neo(config['uri_ubuntu'], config['user'], config['pwd'])
#m.exec(tx_type='create_node', node_class='country',  node_name='New Zealand')

country_list = m.exec('list_nodes_class', node_class='country')
city_list = m.exec('list_nodes_class', node_class='city')
rels_list = m.exec('list_rels')
node_list = country_list+city_list


for nl in node_list:
    nl[0]['key'] = nl[0]['name'].lower().replace(' ', '')


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["FLASK_DEBUG"] = 0
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html',
                           node_list=node_list,
                           rels_list=rels_list)

@app.route('/find_rels', methods=['POST'])
def find_rels():
    node_name = json.loads(request.data)
    rels_dict = m.exec('list_node_rels', node_name=node_name)
    return rels_dict



if __name__ == '__main__':
    app.run(port=5001)














