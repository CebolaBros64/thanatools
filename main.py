from pprint import pprint
import tomllib

if __name__ == '__main__':
    print("=== THANATOOLS ===")

    with open('pdp.toml', 'rb') as f:
        test = tomllib.load(f)
    pprint(test)
