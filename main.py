from pprint import pprint
from panepon.script import Block, Text, ControlCode

if __name__ == '__main__':
    print("=== THANATOOLS ===")

    with open('panepon.toml', 'rb') as toml:
        with open('character_bios.bin', 'rb') as rom:
            test = Block(toml, rom)
    
    binMessages = test.bytes.split(b'\xff')
    messages = []
    
    for binMessage in binMessages:
        message = []
        section = b''
        i = 0

        while i < len(binMessage):
            byte = binMessage[i]

            if byte >= 0xF1 and f"{byte:02x}".upper() in test.game['encoding']['controls']:
                ctrlCode = test.game['encoding']['controls'][f"{byte:02x}".upper()]

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
        

    