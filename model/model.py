import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._idMapCategories={}
        self._graph=nx.DiGraph()
        self._idMapNodes={}

        self._bestPath=[]
        self._bestCost=0

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        categories= DAO.getCategories()
        res=[]
        for c in categories:
            self._idMapCategories[c.category_name]=c
            res.append(c.category_name)
        return res

    def createGraph(self, category, startDate, endDate):
        self._graph.clear()
        nodes=DAO.getNodes(self._idMapCategories[category])
        for node in nodes:
            self._idMapNodes[node.product_id]=node
        self._graph.add_nodes_from(nodes)

        self._putEdges(startDate, endDate)


    def _putEdges(self, startDate, endDate):
        peso=DAO.getEdges(startDate, endDate)
        for nodo1 in peso:
            for nodo2 in peso:
                if nodo1[0] == nodo2[0]:
                    continue
                if nodo1[0] in self._idMapNodes.keys() and nodo2[0] in self._idMapNodes.keys():
                    if self._graph.has_edge(self._idMapNodes[nodo1[0]], self._idMapNodes[nodo2[0]]):
                        continue
                    if nodo1[1]>nodo2[1]:
                        self._graph.add_edge(self._idMapNodes[nodo1[0]], self._idMapNodes[nodo2[0]], weight=nodo2[1]+nodo1[1])
                    elif nodo1[1]<nodo2[1]:
                        self._graph.add_edge(self._idMapNodes[nodo2[0]], self._idMapNodes[nodo1[0]], weight=nodo2[1] + nodo1[1])
                    else:
                        self._graph.add_edge(self._idMapNodes[nodo1[0]],self._idMapNodes[nodo2[0]], weight=nodo2[1]+nodo1[1])
                        self._graph.add_edge(self._idMapNodes[nodo2[0]], self._idMapNodes[nodo1[0]], weight=nodo2[1] + nodo1[1])


    def getInfoGraph(self):
        return len(self._graph.nodes), len(self._graph.edges)
    def bestProducts(self):
        lista_punteggi = []
        for nodo in self._graph.nodes:
            peso_uscente = 0
            for u, v, dati in self._graph.out_edges(nodo, data=True):
                peso_uscente += dati['weight']
            peso_entrante = 0
            for u, v, dati in self._graph.in_edges(nodo, data=True):
                peso_entrante += dati['weight']
            score = peso_uscente - peso_entrante
            lista_punteggi.append((nodo, score))
        lista_ordinata = sorted(lista_punteggi, key=lambda x: x[1], reverse=True)
        return lista_ordinata[:5]
    def getAllNodes(self):
        return self._graph.nodes


    def getCammino(self, source, destination, length):
        partenza=self._idMapNodes[int(source)]
        destinazione=self._idMapNodes[int(destination)]
        lun=int(length)
        self._bestPath=[]
        self._bestCost=0

        parziale=[partenza]

        for vicino in self._graph.neighbors(partenza):
            parziale.append(vicino)
            self._ricorsione(parziale, lun, destinazione)
            parziale.pop()

        return self._bestPath, self._bestCost

    def _ricorsione(self, parziale, length, arrivo):
        if len(parziale)==length+1:
            if parziale[-1]==arrivo:
                peso=self._calcolaPeso(parziale)
                if peso>self._bestCost:
                    self._bestCost=peso
                    self._bestPath=copy.deepcopy(parziale)

            return

        for vicino in self._graph.neighbors(parziale[-1]):
            if vicino not in parziale:
                parziale.append(vicino)
                self._ricorsione(parziale, length, arrivo)
                parziale.pop()

    def _calcolaPeso(self, parziale):
        peso=0
        for n in range(len(parziale)-1):
            peso+=self._graph[parziale[n]][parziale[n+1]]['weight']

        return peso