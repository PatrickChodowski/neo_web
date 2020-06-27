
import yaml
from source.neo import Neo

with open(r'config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
m = Neo(config['uri'], config['user'], config['pwd'])

#country_list = m.exec('list_nodes_class', node_class='country')
#city_list = m.exec('list_nodes_class', node_class='city')
rels_list = m.exec('list_rels')



for key, value in rels_list.items():
    print(rels_list[key]['start_key'])
    print(rels_list[key]['end_key'])



# how the match relationships work
