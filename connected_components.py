

class ConnectedComponents:

    def __init__(self, df):
        self.df = df

    def _get_connected_components(self):
        graph = []
        connected_components = []
        for row in range(len(self.df)):
            if len(self.df.loc[row,'TranscriptHighlights'])!=0:
                connected_components.append(row)
            else:
                if connected_components != []:
                    graph.append(connected_components)
                    connected_components = []
        return graph

    def _merge_related_components(self):
        graphs = self._get_connected_components()
        print(graphs)
        all_graphs = [graphs[0]]
        for graph in range(1, len(graphs)):
            if (graphs[graph][0] - all_graphs[-1][-1]) <= 1:
                all_graphs[-1].extend(graphs[graph])
            else:
                all_graphs.append(graphs[graph])
        return all_graphs

