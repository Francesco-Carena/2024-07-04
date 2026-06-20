import model.model as model

m=model.Model()
forme=m.getShapes(1949)
m.createGraph(1968,"circle")
for node in m._graph.nodes:
    print(node.id)