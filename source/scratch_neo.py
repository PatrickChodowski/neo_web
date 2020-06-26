
import yaml
from source.neo import Neo

with open(r'config.yml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
m = Neo(config['uri'], config['user'], config['pwd'])

country_list = m.exec('list_nodes_class', node_class='country')



country_list[0][0]