import tomllib

controlCodeStart = 0xF1  # Panepon# Should be a parameter in the .toml file, hardcoded for now
controlCodeStart = 0xC4

class TranslationTable:
    def shiftTable(self, tempOffset):
        self.table = {}
        for subTable in self.encoding:
            for i, glyph in enumerate(subTable['glyphs']):
                if subTable['offset']+i >= controlCodeStart:
                    break
                else:
                    glyph = subTable['glyphs'][i]
                    self.table[subTable['offset']+i] = glyph
            # print(subTable)
        # print(self.table)

    def __init__(self, encoding):
        self.encoding = encoding
        self.shiftTable(0)

    def __str__(self):
        return self.table
    
    def __getitem__(self, i):
        if i in self.table:
            return self.table[i]
        else:
            return f"\\x{i:02x}"

class Section:
    def __init__(self, bytes):
        self.bytes = bytes

    def as_bytes(self):
        return self.bytes

class Text(Section):
    def __init__(self, bytes):
        self.type = 'text'
        Section.__init__(self, bytes)

    # def __str__(self):
        # return self.bytes
        # return ''.join([f"\\x{i:02x}" for i in self.as_bytes()])

    def as_text(self, translationTable):
        _str = ''
        for byte in self.bytes:
            _str += translationTable[byte]
        return _str
        # return self.__str__()

class ControlCode(Section):
    def __init__(self, bytes, game_toml):
        self.type = 'control_code'
        self.codeByte = bytes[0]
        self.codeName = game_toml['encoding']['controls'][f"{self.codeByte:02x}".upper()]['name']
        self.paramsBytes = bytes[1:]
        Section.__init__(self, bytes)

    def __str__(self):
        if len(self.bytes) > 1:
            return f"<{self.codeName} params='{self.paramsBytes.hex()}'/>"
        else:
            return f"<{self.codeName} />"
    
    def as_text(self, _):
        return self.__str__()
    
class Message:
    def __init__(self, game_toml, bytes):
        self.index = 0
        self.encoding = game_toml['encoding']['table']
        self.sections = []

        # Split message into sections
        section = b''
        i = 0

        while i < len(bytes):
            byte = bytes[i]

            if byte >= controlCodeStart and f"{byte:02x}".upper() in game_toml['encoding']['controls']:
                ctrlCode = game_toml['encoding']['controls'][f"{byte:02x}".upper()]

                if section != b'':
                    self.sections.append(Text(section))
                    section = b''

                if 'length' in ctrlCode:
                    self.sections.append(ControlCode(bytes[i:i+ctrlCode['length']+1], game_toml))
                    i += ctrlCode['length'] + 1
                else:
                    section += byte.to_bytes()
                    # section += ctrlCode['name']
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
    
    def __str__(self):
        translationTable = TranslationTable(self.encoding)

        returnVal = ''
        for section in self.sections:
            if section.type == 'control_code' and section.codeName == 'table':
                translationTable.shiftTable(section.paramsBytes[0])

            returnVal += section.as_text(translationTable)

        return returnVal

class Block:
    def __init__(self, game_toml, rom, start_offset=0, length=None):
        self.game = tomllib.load(game_toml)['game']

        rom.seek(start_offset)
        self.bytes = rom.read(length)

        # Split block into messages
        binMessages = self.bytes.split(b'\xff')
        self.messages = []
        
        for binMessage in binMessages:
            self.messages.append(Message(self.game, binMessage))
    
