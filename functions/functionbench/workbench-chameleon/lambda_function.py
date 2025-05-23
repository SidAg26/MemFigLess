from time import time
import six
import json
from chameleon import PageTemplate


BIGTABLE_ZPT = """\
<table xmlns="http://www.w3.org/1999/xhtml"
xmlns:tal="http://xml.zope.org/namespaces/tal">
<tr tal:repeat="row python: options['table']">
<td tal:repeat="c python: row.values()">
<span tal:define="d python: c + 1"
tal:attributes="class python: 'column-' + %s(d)"
tal:content="python: d" />
</td>
</tr>
</table>""" % six.text_type.__name__


def lambda_handler(event, context):

    try:
        if 'body' in event.keys():
            data = json.loads(event['body'])
            num_of_rows = int(data['num_of_rows'])
            num_of_cols = int(data['num_of_cols'])
        elif 'num_of_rows' in event.keys():
            num_of_rows = int(event['num_of_rows'])
            num_of_cols = int(event['num_of_cols'])
    except ValueError as e:
        raise e
    except Exception as e:
        raise e

    start = time()
    tmpl = PageTemplate(BIGTABLE_ZPT)

    data = {}
    for i in range(num_of_cols):
        data[str(i)] = i

    table = [data for x in range(num_of_rows)]
    options = {'table': table}

    data = tmpl.render(options=options)
    latency = time() - start

    # result = json.dumps({'latency': latency, 'data': data})
    result = json.dumps({'latency': latency, 'num_of_rows': num_of_rows,
                         'num_of_cols': num_of_cols }) # remove 'data' - might throw payloadSize error
    
    response = {
                "isBase64Encoded": "false",
                "statusCode": 200,
                "body": result,
                "headers": {
                "content-type": "application/json"
                }
            }
    
    return response