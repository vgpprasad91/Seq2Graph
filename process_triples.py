import pandas as pd
import json

df = pd.read_csv("triplets.csv")
graph_nodes = []
graph_links = []
cnt  = 1

# Get the graph ids
for row in range(len(df)):
    source_node = {"name": cnt, "label":df.loc[row,"triplet1"],"id": cnt}
    src_node_id = cnt
    cnt += 1
    destination_node = {"name": cnt, "label":df.loc[row,"triplet3"], "id": cnt}
    dest_node_id = cnt
    graph_nodes.append(source_node)
    graph_nodes.append(destination_node)
    link = {"source": src_node_id, "target": dest_node_id, "type": df.loc[row, "triplet2"]}
    graph_links.append(link)

with open("./d3rdf/graph.json","w") as f:
    graph = {"nodes": graph_nodes, "links": graph_links}
    json.dump(graph, f)