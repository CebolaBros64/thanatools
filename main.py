from pprint import pprint
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

if __name__ == '__main__':
    print("=== THANATOOLS ===")

    with open('panepon.toml', 'rb') as f:
        test = tomllib.load(f)

    with open('character_bios.bin', 'rb') as f:
        binBlock = f.read()
    
    binMessages = binBlock.split(b'\xff')
    messages = []
    
    for binMessage in binMessages:
        message = []
        section = b''
        i = 0

        while i < len(binMessage):
            byte = binMessage[i]

            if byte >= 0xF1 and f"{byte:02x}".upper() in test['game']['encoding']['controls']:
                ctrlCode = test['game']['encoding']['controls'][f"{byte:02x}".upper()]

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

        messages.append(message)

    # pprint(messages)
    for i, message in enumerate(messages):
        print(f"Message {i}")

        for section in message:
            print(section.as_bytes())
            # print(section.as_text())
        

    