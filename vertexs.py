from utils import *
import json
import pandas as pd
import sys
# config
"""
{prop1: {
type: "Int"
prop: 0.8
},
prop2: {
type: "String",
length: 40,
prop: 1,
primary: true
},
prop3: {
type: "Long",
prop: 0.7
},
prop4: {
type: "String",
length: 50,
prop: 0.8
}
}
"""

def getRandomVertex(config):
    rst = dict()
    for key, value in config.items():
        if value['type'] == "Int" and crap(value['prop']):
            rst[key] = getRandomInt()
        elif value['type'] == "Long" and crap(value['prop']):
            rst[key] = getRandomLong()
        elif value['type'] == "String" and crap(value['prop']):
            rst[key] = getRandomStr(value['length'])
    return rst
def getRandomEdge(v1, v2, config):
    rst = dict()
    for key, value in config.items():
        if value['type'] == "Int" and crap(value['prop']):
            rst[key] = getRandomInt()
        elif value['type'] == "Long" and crap(value['prop']):
            rst[key] = getRandomLong()
        elif value['type'] == "String" and crap(value['prop']):
            rst[key] = getRandomStr(value['length'])
    rrst = dict()
    rrst['start'] = v1
    rrst['end'] = v2
    rrst['edge'] = rst
    return rrst
def getVertexs(config, length):
    primaryName = ""
    for key, value in config.items():
        if "primary" in value:
            primaryName = key
    rst = dict()
    for i in range(length):
        vertex = getRandomVertex(config)
        rst[vertex[primaryName]] = vertex
    return rst

def getGraph(vertexConfig, vertexLength, edgeConfig, edgesPerVertex):
    vertexs = getVertexs(vertexConfig, vertexLength)
    edges = []
    primaryIds = list(vertexs.keys())
    for key, value in vertexs.items():
        for i in range(edgesPerVertex):
            index = random.randint(0, len(primaryIds) - 1)
            primaryId = primaryIds[index]
            if primaryId != key:
                edge = getRandomEdge(key, primaryId, edgeConfig)
                edges.append(edge)
    graph = dict()
    graph['V'] = vertexs
    graph['E'] = edges
    return graph

def saveToCsv(vertexConfig, vertexLength, edgeConfig, edgesPerVertex):
    graph = getGraph(vertexConfig, vertexLength, edgeConfig, edgesPerVertex)
    vertexs = graph['V']
    edges = graph['E']
    vertexProps = list(vertexConfig.keys())
    tmpVertes = []
    for key, value in vertexs.items():
        tmp = []
        for prop in vertexProps:
            if prop in value:
                tmp.append(value[prop])
            else:
                tmp.append(None)
        tmp.append(key)
        tmpVertes.append(tmp)
    columns = []
    for key, value in vertexConfig.items():
        if value['type'] == "INT" or value['type'] == "Long":
            columns.append(key + ":int")
        else:
            columns.append(key)
    columns.append("pk:ID")

    vertexPd = pd.DataFrame(tmpVertes, columns=columns)
    vertexPd[':LABEL'] = "PyVertex"
    edgeProps = list(edgeConfig.keys())
    tmpEdges = []
    for edge in edges:
        tmp = []
        for prop in edgeProps:
            if prop in edge['edge']:
                tmp.append(edge['edge'][prop])
            else:
                tmp.append(None)
        tmp.append(edge['start'])
        tmp.append(edge['end'])
        tmpEdges.append(tmp)
    columns = []
    for key, value in edgeConfig.items():
        if value['type'] == "INT" or value['type'] == "Long":
            columns.append(key + ":int")
        else:
            columns.append(key)
    columns.append(":START_ID")
    columns.append(":END_ID")
    edgePd = pd.DataFrame(tmpEdges, columns=columns)
    edgePd[':Type'] = "PyEdge"
    edgePd.to_csv("./edges_" + sys.argv[1] + "_" + sys.argv[2] + ".csv", index=None)
    vertexPd.to_csv("./vertexs_" + sys.argv[1] + "_" + sys.argv[2] + ".csv", index=None)





if __name__ == '__main__':
    vertexConfig = """
    {
    "prop1": {
    "type": "Int",
    "prop": 0.8
    },
    "prop2": {
    "type": "String",
    "length": 50,
    "prop": 1,
    "primary": true
    },
    "prop3": {
    "type": "Int",
    "prop": 0.9
    }
    }
    """
    edgeConfig = """
    {
    "prop1": {
    "type": "Int",
    "prop": 0.8
    },
    "prop2": {
    "type": "String",
    "length": 50,
    "prop": 1,
    "primary": true
    },
    "prop3": {
    "type": "Int",
    "prop": 0.9
    }
    }
    """
    saveToCsv(json.loads(vertexConfig), int(sys.argv[1]), json.loads(edgeConfig), int(sys.argv[2]))

