# GRAPH PAGERANK
import datetime
import igraph


def lambda_handler(event, context):
    size = event['n'] if 'n' in event else 1000
    size = int(size) if isinstance(size, str) else size

    graph_generating_begin = datetime.datetime.now()
    graph = igraph.Graph.Barabasi(size, 100)
    graph_generating_end = datetime.datetime.now()

    process_begin = datetime.datetime.now()
    result = graph.pagerank()
    process_end = datetime.datetime.now()

    graph_generating_time = (graph_generating_end - graph_generating_begin) / datetime.timedelta(microseconds=1)
    process_time = (process_end - process_begin) / datetime.timedelta(microseconds=1)

    resp = {
        'result': result[0],
        'measurement': {
            'graph_generating_time': graph_generating_time,
            'compute_time': process_time
        }
    }

    return resp