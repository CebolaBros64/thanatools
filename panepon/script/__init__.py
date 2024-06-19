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
    
class Message():
    def __init__(self, sectionArray):
        self.index = 0
        self.array = sectionArray

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.index == len(self.array):
            raise StopIteration
        returnVal = self.array[self.index]
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
            sections = []
            section = b''
            i = 0

            while i < len(binMessage):
                byte = binMessage[i]

                if byte >= 0xF1 and f"{byte:02x}".upper() in self.game['encoding']['controls']:
                    ctrlCode = self.game['encoding']['controls'][f"{byte:02x}".upper()]

                    if section != b'':
                        sections.append(Text(section))
                        section = b''

                    if 'length' in ctrlCode:
                        sections.append(ControlCode(binMessage[i:i+ctrlCode['length']+1], self.game))
                        i += ctrlCode['length'] + 1
                    else:
                        section += byte.to_bytes()
                        i += 1
                else:
                    section += byte.to_bytes()
                    i += 1

            self.messages.append(Message(sections))
    
