import uuid

_id_cache = []


def new_id():
    x = str(uuid.uuid4())[:6].upper()
    while x in _id_cache:
        x = str(uuid.uuid4())[:6].upper()

    _id_cache.append(x)
    return x
