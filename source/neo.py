
class Neo:
    def __init__(self, uri, user, pwd):
        self.driver = self._connect(uri, user, pwd)
        self.session = self.driver.session()
        self._define_funcs()

    def _define_funcs(self):
        self._func_dict = {'set_property': self._set_property,
                          'create_node': self._create_if_doesnt_exist,
                          'create_rel': self._create_rel,
                          'list_nodes_class': self._list_nodes_class,
                          'list_node_rels': self._list_node_rels,
                          'list_rels': self._list_rels,
                          'clean_db': self._clean_db,
                          'del_class': self._del_class,
                          'del_node': self._del_node}

    def exec(self, tx_type, **kwargs):
        tx = self.session.begin_transaction()
        res = self._func_dict[tx_type](tx=tx, **kwargs)
        tx.commit()
        return res

    @staticmethod
    def _connect(uri, user, pwd):
        from neo4j import GraphDatabase
        return GraphDatabase.driver(uri=uri, auth=(user, pwd))

    @staticmethod
    def _node_exists(tx, node_name):
        query = f"MATCH(n {{name:'{node_name}'}}) RETURN n.name"
        result = tx.run(query)
        results = [res for res in result]
        if results.__len__() > 0:
            return True
        else:
            return False

    def _create_if_doesnt_exist(self, tx, node_class, node_name):
        if self._node_exists(tx, node_name):
            print(f'{node_name} exists')
        else:
            self._create_node(tx, node_class=node_class, node_name=node_name)

    def _create_node(self, tx, node_class, node_name):
        query = f"CREATE(a: {node_class} {{name:'{node_name}'}})"
        print(query)
        tx.run(query)

    def _set_property(self, tx, node_name, node_prop, prop):
        if self._node_exists(tx, node_name):
            query = f"MATCH(n {{name:'{node_name}'}}) SET n.{node_prop} = '{prop}'"
            print(query)
            tx.run(query)
        else:
            pass

    def _create_rel(self, tx, nc1, n1, rel, nc2, n2):
        self._create_if_doesnt_exist(tx, node_class=nc1, node_name=n1)
        self._create_if_doesnt_exist(tx, node_class=nc2, node_name=n2)

        query = f"""MATCH (a:{nc1}),(b:{nc2})
        WHERE a.name = '{n1}' AND b.name = '{n2}'
    
        CREATE (a)-[r:{rel} {{name: '{rel}'}}]->(b)
        RETURN type(r), r.name"""
        print(query)
        tx.run(query)

    @staticmethod
    def _list_nodes_class(tx, node_class):
        node_list = list()
        query = f'MATCH (n:{node_class}) RETURN {{id: id(n), name:n.name, label:labels(n), props:properties(n) }}'
        print(query)
        result = tx.run(query)
        for res in result:
            node_list.append(res)
        return node_list

    @staticmethod
    def _list_node_rels(tx, node_name):
        rels_dict = dict()
        query = f"MATCH(n {{name:'{node_name}'}})-[r] - (b) RETURN r, {{end_id: id(b), end_name:b.name, end_label:labels(b), end_props:properties(b) }}"
        print(query)
        result = tx.run(query)
        for res in result:
            resd = dict()
            resd['rel_name'] = res['r']['name']
            resd['rel_type'] = res['r'].type
            resd['rel_id'] = res['r'].id
            resd['end_name'] = res[1]['end_name']
            resd['end_node_id'] = res[1]['end_id']
            resd['end_label'] = res[1]['end_label']
            resd['end_props'] = res[1]['end_props']

            rels_dict[f"rel_{node_name}_{resd['rel_name']}_{resd['end_name']}"] = resd
        return rels_dict

    @staticmethod
    def _list_rels(tx):
        rels_dict = dict()
        query = f"MATCH (n) -[r] -> (b) RETURN {{start_id: id(n), start_name:n.name, start_label:labels(n), start_props:properties(n) }}, r, {{end_id: id(b), end_name:b.name, end_label:labels(b), end_props:properties(b) }}"
        print(query)
        result = tx.run(query)
        for res in result:
            resd = dict()
            resd['start_name'] =    res[0]['start_name']
            resd['start_node_id'] = res[0]['start_id']
            resd['start_label'] =   res[0]['start_label']
            resd['start_props'] =   res[0]['start_props']
            resd['rel_name'] = res['r']['name']
            resd['rel_type'] = res['r'].type
            resd['rel_id'] = res['r'].id
            resd['end_name'] = res[2]['end_name']
            resd['end_node_id'] = res[2]['end_id']
            resd['end_label'] = res[2]['end_label']
            resd['end_props'] = res[2]['end_props']

            resd['start_key'] = res[0]['start_name'].lower().replace(' ', '')
            resd['end_key'] = res[2]['end_name'].lower().replace(' ', '')

            rels_dict[f"rel_{resd['start_name']}_{resd['rel_name']}_{resd['end_name']}"] = resd
        return rels_dict


    @staticmethod
    def _clean_db(tx):
        query = 'MATCH (n) DETACH DELETE n'
        print(query)
        tx.run(query)

    @staticmethod
    def _del_class(tx, node_class):
        query = f'MATCH (n:{node_class}) DELETE n'
        print(query)
        tx.run(query)

    @staticmethod
    def _del_node(tx, node_name):
        query = f"MATCH(n {{name:'{node_name}'}}) DELETE n"
        print(query)
        tx.run(query)

