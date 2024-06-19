import tomllib

class Section:
    def __init__(self, bytes):
        self.bytes = bytes

    def as_bytes(self):
        return self.bytes

class Text(Section):
    # def __str__(self):
        # return
        # return ''.join([f"\\x{i:02x}" for i in self.as_bytes()])

    def as_text(self):
        return self.__str__()

class ControlCode(Section):
    def __init__(self, bytes, game_toml):
        self.codeByte = bytes[0]
        self.codeName = game_toml['encoding']['controls'][f"{self.codeByte:02x}".upper()]['name']
        self.paramsBytes = bytes[1:]
        Section.__init__(self, bytes)

    def __str__(self):
        if len(self.bytes) > 1:
            return f"<{self.codeName} params='{self.paramsBytes.hex()}'/>"
        else:
            return f"<{self.codeName} />"
    
    def as_text(self):
        return self.__str__()
    
class Message:
    def __init__(self, game_toml, bytes):
        self.index = 0
        self.sections = []
        section = b''
        i = 0

        while i < len(bytes):
            byte = bytes[i]

            if byte >= 0xF1 and f"{byte:02x}".upper() in game_toml['encoding']['controls']:
                ctrlCode = game_toml['encoding']['controls'][f"{byte:02x}".upper()]

                if section != b'':
                    self.sections.append(Text(section))
                    section = b''

                if 'length' in ctrlCode:
                    self.sections.append(ControlCode(bytes[i:i+ctrlCode['length']+1], game_toml))
                    i += ctrlCode['length'] + 1
                else:
                    section += byte.to_bytes()
                    i += 1
            else:
                section += byte.to_bytes()
                i += 1

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index == len(self.sections):
            raise StopIteration
        returnVal = self.sections[self.index]
        self.index += 1
        return returnVal
    
    # def __str__(self):
    #     return

class Block:
    def __init__(self, game_toml, rom, start_offset=0, length=None):
        self.game = tomllib.load(game_toml)['game']

        rom.seek(start_offset)
        self.bytes = rom.read(length)

        binMessages = self.bytes.split(b'\xff')
        self.messages = []
        
        for binMessage in binMessages:
            self.messages.append(Message(self.game, binMessage))
    
