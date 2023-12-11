import json

from bson import json_util


def json_dump(data, fileName):
    with open('./'+fileName+'.json', 'w', encoding='utf-8') as out:
        out.write(json_util.dumps(data, ensure_ascii=False))