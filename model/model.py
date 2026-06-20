import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapNodes={}

        self._bestPoints=0
        self._bestPath=[]

    def getAllYears(self):
        return DAO.getAllYears()

    def getShapes(self, anno):
        return DAO.getShapes(anno)

    def createGraph(self,anno, forma):
        self._graph.clear()
        self._idMapNodes = {}

        nodes=DAO.getSightings(anno, forma)
        self._graph.add_nodes_from(nodes)
        for node in nodes:
            self._idMapNodes[node.id]=node

        self._addEdges()

    def _addEdges(self):
        for node in self._graph.nodes:
            for node1 in self._graph.nodes:
                if node == node1 or self._graph.has_edge(node1, node) or self._graph.has_edge(node, node1):
                    continue
                if node1.state==node.state:
                    if node.datetime < node1.datetime:
                        self._graph.add_edge(node, node1)
                    elif node.datetime > node1.datetime:
                        self._graph.add_edge(node1, node)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getDettagliComponenti(self):
        componenti = list(nx.weakly_connected_components(self._graph))
        numero_componenti = len(componenti)

        componente_maggiore = max(componenti, key=len)

        return numero_componenti, componente_maggiore


    def searchPath(self):
        self._bestPath=[]
        self._bestPoints=0

        for nodo in self._graph.nodes:
            self._ricorsione([nodo], 100)

        return self._bestPoints, self._bestPath

    def _ricorsione(self, parziale, punteggio):
        if punteggio > self._bestPoints:
            self._bestPoints=punteggio
            self._bestPath = copy.deepcopy(parziale)

        ultimo_nodo = parziale[-1]
        for vicino in self._graph.neighbors(ultimo_nodo):
            if vicino.duration > ultimo_nodo.duration:
                mese_vicino = vicino.datetime.month
                mese_ultimo = ultimo_nodo.datetime.month
                conteggio_mese = sum(1 for n in parziale if n.datetime.month == mese_vicino)
                if conteggio_mese < 3:
                    nuovo_punteggio = punteggio + 100
                    if mese_vicino == mese_ultimo:
                        nuovo_punteggio += 200

                    parziale.append(vicino)
                    self._ricorsione(parziale, nuovo_punteggio)
                    parziale.pop()