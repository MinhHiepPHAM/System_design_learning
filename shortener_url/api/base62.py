import string

BASE62 = tuple(string.ascii_letters + string.digits)

NUM2KEY_MAP = {i: ch for i,ch in enumerate(BASE62)}
KEY2NUM_MAP = {ch: i for i, ch in enumerate(BASE62)}

def encode(num: int, base: int=62) -> str:
    keys = []
    while(num > 0):
        keys.append(NUM2KEY_MAP[num%base])
        num //= base

    return ''.join(keys[::-1])

def decode(keys: str, base: int=62) -> int:
    if len(keys) == 0:
        raise ValueError("The key must not be empty")
    num = 0
    for i, ch in enumerate(keys[::-1]):
        num += KEY2NUM_MAP[ch]*(base**i)

    return num

if __name__ == '__main__':
    print('125 to X62: ', encode(125))
    print('cb X62 to int:', decode('cb'))

    print('19158 to X62: ', encode(19158))
    print('e9a to int', decode('e9a'))

