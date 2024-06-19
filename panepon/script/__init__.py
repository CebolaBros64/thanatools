import tomllib

class Block:
    def __init__(self, game_toml, rom, length=None, start_offset=0):
        self.game = tomllib.load(game_toml)['game']

        rom.seek(start_offset)
        self.bytes = rom.read(length)

class Section:
    def __init__(self, bytes):
        self.bytes = bytes

    def as_bytes(self):
        return self.bytes

class Text(Section):
    def as_text(self):
        pass

class ControlCode(Section):
    def as_text(self):
        pass
