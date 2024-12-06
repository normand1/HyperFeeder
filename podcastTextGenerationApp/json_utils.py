from json import JSONEncoder, dump, dumps


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        return super().default(obj)


def dump_json(obj, file, **kwargs):
    """Wrapper for json.dump that always uses CustomJSONEncoder"""
    return dump(obj, file, cls=CustomJSONEncoder, **kwargs)


def dumps_json(obj, **kwargs):
    """Wrapper for json.dumps that always uses CustomJSONEncoder"""
    return dumps(obj, cls=CustomJSONEncoder, **kwargs)
