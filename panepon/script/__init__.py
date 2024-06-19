import tomllib

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

class Block:
    def __init__(self, game_toml, rom, start_offset=0, length=None):
        self.game = tomllib.load(game_toml)['game']

        rom.seek(start_offset)
        self.bytes = rom.read(length)

        binMessages = self.bytes.split(b'\xff')
        self.messages = []
        
        for binMessage in binMessages:
            message = []
            section = b''
            i = 0

            while i < len(binMessage):
                byte = binMessage[i]

                if byte >= 0xF1 and f"{byte:02x}".upper() in self.game['encoding']['controls']:
                    ctrlCode = self.game['encoding']['controls'][f"{byte:02x}".upper()]

                    if section != b'':
                        message.append(Text(section))
                        section = b''

                    if 'length' in ctrlCode:
                        message.append(ControlCode(binMessage[i:i+ctrlCode['length']+1]))
                        i += ctrlCode['length'] + 1
                    else:
                        section += byte.to_bytes()
                        i += 1
                else:
                    section += byte.to_bytes()
                    i += 1

            self.messages.append(message)
