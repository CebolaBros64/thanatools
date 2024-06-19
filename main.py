from pprint import pprint
from panepon.script import Block

if __name__ == '__main__':
    print("=== THANATOOLS ===")

    with open('panepon.toml', 'rb') as toml:
        # with open('character_bios.bin', 'rb') as rom:
        #     test = Block(toml, rom)

        with open('games/Panel de Pon (World) (Ja) (Rev 1) (Virtual Console, Switch Online).sfc', 'rb') as rom:
            test = Block(toml, rom, 0x51637, 0x796)

    for i, message in enumerate(test.messages):
        print(f"= Message {i} =")

        for i2, section in enumerate(message):
            print(f"Section {i2:02}: {section.as_bytes()}")
            # print(section.as_text())
