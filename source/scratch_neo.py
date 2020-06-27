
import yaml
from source.neo import Neo

with open(r'config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
m = Neo(config['uri'], config['user'], config['pwd'])

#country_list = m.exec('list_nodes_class', node_class='country')
#city_list = m.exec('list_nodes_class', node_class='city')
rels_list = m.exec('list_node_rels', node_name='Poland')


node_list = country_list+city_list
country_list[6][0]['id']

country_list[0].__dir__()


country_list[0].keys()
country_list[0].values()
country_list[0].items()

country_list[0][0]['name']
country_list[0][0]['id']



a.decode('UTF-8')
