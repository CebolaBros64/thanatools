from pprint import pprint
from panepon.script import Block

if __name__ == '__main__':
    print("=== THANATOOLS ===")

    with open('panepon.toml', 'rb') as toml:
        with open('games/Panel de Pon (World) (Ja) (Rev 1) (Virtual Console, Switch Online).sfc', 'rb') as rom:
            test = Block(toml, rom, 0x51637, 0x796)

    # with open('tattack.toml', 'rb') as toml:
    #     with open('games/Tetris Attack (USA) (En,Ja).sfc', 'rb') as rom:
    #         test = Block(toml, rom, 0xCAE5B, 0xA2E)

    for i, message in enumerate(test.messages):
        txtMessage = str(message)
        print()
        print(f"= Message {i} =")
        print(txtMessage)
