#!/usr/bin/env python3

# UTF-8(1993) (cuz in RFC 3629 (in 2003) it was restricted) so it can fit up to 31-bit unsigned integer
def encode_to_utf8(number):
    if number < 0 or number > 0x7FFFFFFF:
        raise ValueError("Number must be a 31-bit unsigned integer.")
    
    if number <= 0x7F:
        return bytes([number])
    
    elif number <= 0x7FF:
        byte1 = 0xC0 | (number >> 6)
        byte2 = 0x80 | (number & 0x3F)
        return bytes([byte1, byte2])
    
    elif number <= 0xFFFF:
        byte1 = 0xE0 | (number >> 12)
        byte2 = 0x80 | ((number >> 6) & 0x3F)
        byte3 = 0x80 | (number & 0x3F)
        return bytes([byte1, byte2, byte3])
    
    elif number <= 0x1FFFFF:
        byte1 = 0xF0 | (number >> 18)
        byte2 = 0x80 | ((number >> 12) & 0x3F)
        byte3 = 0x80 | ((number >> 6) & 0x3F)
        byte4 = 0x80 | (number & 0x3F)
        return bytes([byte1, byte2, byte3, byte4])
    
    elif number <= 0x3FFFFFF:
        byte1 = 0xF8 | (number >> 24)
        byte2 = 0x80 | ((number >> 18) & 0x3F)
        byte3 = 0x80 | ((number >> 12) & 0x3F)
        byte4 = 0x80 | ((number >> 6) & 0x3F)
        byte5 = 0x80 | (number & 0x3F)
        return bytes([byte1, byte2, byte3, byte4, byte5])
    
    elif number <= 0x7FFFFFFF:
        byte1 = 0xFC | (number >> 30)
        byte2 = 0x80 | ((number >> 24) & 0x3F)
        byte3 = 0x80 | ((number >> 18) & 0x3F)
        byte4 = 0x80 | ((number >> 12) & 0x3F)
        byte5 = 0x80 | ((number >> 6) & 0x3F)
        byte6 = 0x80 | (number & 0x3F)
        return bytes([byte1, byte2, byte3, byte4, byte5, byte6])
    
    else:
        raise ValueError("Number exceeds the valid range for a 31-bit unsigned integer.")

def main():
    with open('unifont_all-15.0.05.hex', 'r') as fin:
        with open('unifont_all-15.0.05.bin', "wb") as fout:
            data = [{'width':8, 'height':16, 'data':[]}, {'width':16, 'height':16, 'data':[]}]
            for key, value in sorted({int(line.split(':')[0], 16):bytes.fromhex(line.split(':')[1]) for line in fin.readlines() if len(line.split(':')) == 2}.items()):
                data[1 if len(value) > 16 else 0]['data'].append((encode_to_utf8(key), value))
            fout.write((0).to_bytes(4, 'big'))
            for collection in data:
                fout.write(collection['width'].to_bytes(1, 'big'))
                fout.write(collection['height'].to_bytes(1, 'big'))
                fout.write(len(collection['data']).to_bytes(4, 'big'))
                fout.write((14).to_bytes(1, 'big'))
                for character in collection['data']:
                    fout.write(character[0])
                for character in collection['data']:
                    fout.write(character[1])

if __name__ == "__main__":
    main()