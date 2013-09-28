import uuid


class Player(object):

    def __init__(self, name="", hand=[]):
        self.id = str(uuid.uuid4())[:6].upper()
        self.name = name
        self.hand = hand
        self.lamp = False
