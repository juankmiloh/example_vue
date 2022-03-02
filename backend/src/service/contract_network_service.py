import pandas as pd
import networkx as nx
import datetime
from flask import abort
from ..repository import ContractNetworkRepository
from ..util.web_util import to_date
from ..util.web_util import add_wrapper

class ContractNetworkService:

    def get_graph(self, start_date, end_date, modality, query_node, contract_network_repository: ContractNetworkRepository):

        df = contract_network_repository.find_contracts_by_date(start_date, end_date, modality)

        df['nombre_usuario_final'] = df['nombre_usuario_final'].str.upper().str.replace('.', '', regex=False).str.replace(' SAS', '').str.replace(' SA', '').str.replace(' ESP', '').str.strip().str.replace('TERMOBARRANQUILLA', 'TEBSA')
        df['nombre_vendedor'] = df['nombre_vendedor'].str.upper().str.replace('.', '', regex=False).str.replace(' SAS', '').str.replace(' SA', '').str.replace(' ESP', '').str.strip().str.replace('TERMOBARRANQUILLA', 'TEBSA')
        df['nombre_comprador'] = df['nombre_comprador'].str.upper().str.replace('.', '', regex=False).str.replace(' SAS', '').str.replace(' SA', '').str.replace(' ESP', '').str.strip().str.replace('TERMOBARRANQUILLA', 'TEBSA')

        if query_node:
            df = df[df['nombre_usuario_final'] == query_node]
            df.reset_index(inplace=True)

        G1 = nx.from_pandas_edgelist(df, source='nombre_vendedor', target='nombre_comprador', edge_attr=['cantidad', 'precio', 'fecha_inicial', 'fecha_final'], create_using=nx.DiGraph())
        G2 = nx.from_pandas_edgelist(df, source='nombre_comprador', target='nombre_usuario_final', edge_attr=['cantidad', 'precio', 'fecha_inicial', 'fecha_final'], create_using=nx.DiGraph()) 
        G = nx.compose(G1, G2)

        if query_node:
            filtered_nodes = set()
            for node in G.nodes:
                if nx.has_path(G, node, query_node):
                    if nx.shortest_path_length(G, node, query_node) <= 2:
                        filtered_nodes.add(node)
            G = G.subgraph(filtered_nodes)

        return self._serialize_df(df, G, query_node) 
    
    def _serialize_df(self, df, G, query_node=None):

        markets = {query_node: query_node}
        for row in range(len(df)):
            for col in ['nombre_usuario_final', 'nombre_comprador', 'nombre_vendedor']:
                if df.loc[row, col] != query_node:
                    markets[df.loc[row, col]] = df.loc[row, 'mercado']

        categories = {query_node: 0, 'Primario': 1, 'Secundario': 2}

        nodes = [{
            'name': n.replace(' ', '\n'), 
            'category': categories[markets[n]], 
            'value': 5.0, 
            'symbolSize': 60.0 if n != query_node else 80.0,
            'label': { 
                'show': True, 
                'fontSize': 8
            }
        } for n in G.nodes]

        nodes_dict = {e:i for i, e in enumerate(G.nodes)}

        categories = [
            { 'name': query_node },
            { 'name': 'Primario' },
            { 'name': 'Secundario' }
        ]

        links = [{
            'source': nodes_dict[e[0]], 
            'target': nodes_dict[e[1]],
            'amount': float(e[2]['cantidad'])/1000,
            'price': float(e[2]['precio']),
            'label': { 
                'show': True, 
                'fontSize': 6, 
                'formatter': '{:.2f} GBTUD \n {:.2f} USD/MBTU'.format(
                        float(e[2]['cantidad'])/1000, 
                        float(e[2]['precio'])
                        #e[2]['fecha_inicial'], 
                        #e[2]['fecha_final']
                    ) 
            }
        } 
        for e in G.edges.data()]
        agents = [{'id':str(n) , 'text':str(n)} for n in G.nodes]
        agents = [{'id':None , 'text':'Seleccione un agente'}] + agents

        indicator = {
            'id':'contract_network',
            'agents': agents,   
            'nodes': nodes, 
            'links': links,  
            'categories': categories
        }

        return add_wrapper(indicator)
