

class Game(object):
    def __init__(self, id, title, platform=None, platform_id=None, info=None, release_date=None, developer=None, publisher=None):
        self.id = id
        self.title = title
        self.platform = platform
        self.platform_id = platform_id
        self.info = info
        self.release_date = release_date
        self.developer = developer
        self.publisher = publisher

    @classmethod
    def from_dict(cls, data):
        return Game(id = int(data.get("game_id")),
                    title = data.get("game_title"),
                    platform = str(data.get("platform")),
                    platform_id = int(data.get("platform_id")),
                    info = str(data.get("info")),
                    release_date = str(data.get("release_date")),
                    developer = str(data.get("developer")),
                    publisher = str(data.get("publisher"))) 

class Platform(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def from_dict(cls, data):
        return Platform(id = int(data.get("platform_id")),
                        name = str(data.get("platform_name")))

class Relation(object):
    def __init__(self, g1_id, g2_id):
        self.g1_id = g1_id
        self.g2_id = g2_id

    @classmethod
    def from_dict(cls, data):
        return Relation(id = int(data.get("relation_id")),
                        g1_id = int(data.get("g1_id")),
                        g2_id = int(data.get("g2_id")))