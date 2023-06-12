#!/usr/bin/env python3

# UTF-8(1993) (cuz in RFC 3629 (in 2003) it was restricted) so it can fit up to 31-bit unsigned integer
def encode_to_utf8(number: int) -> bytes:
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

from PIL import Image
import json

def bits_to_bytes(bits_count: int):
    return bits_count // 8 + (1 if (bits_count % 8) > 0 else 0)

def get_bits_from_png(img: Image.Image, x: int, y: int, width: int, height: int) -> bytes:
    bitmap = bytearray(bits_to_bytes(width * height))
    for index in range(0, width * height):
        currentX = index % width + x
        currentY = index // width + y
        bitmap[index // 8] |= (0x1 << (7 - index % 8)) if img.getpixel((currentX, currentY))[3] else 0
    return bytes(bitmap)

def main():
    for inFileName, outFileName in [("default.json", "minecraftFont-default.bin"), ("sga.json", "minecraftFont-sga.bin"), ("illageralt.json", "minecraftFont-illageralt.bin")]:
        with open(inFileName, 'r') as fin:
            with open(outFileName, "wb") as fout:
                data = []
                jsonData = json.load(fin)
                for collection in jsonData:
                    characters = []
                    img: Image.Image|None = None
                    space = False
                    if collection['space'] if 'space' in collection else False:
                        space = True
                    else:
                        img = Image.open(collection['file']).convert('RGBA')
                    for lineIndex, line in enumerate(collection['chars']):
                        for characterIndex, character in enumerate(line):
                            imgBytes = b''
                            if space:
                                imgBytes = b'\0' * bits_to_bytes(collection['width'] * collection['height'])
                            else:
                                imgBytes = get_bits_from_png(img, characterIndex * collection['width'], lineIndex * collection['height'], collection['width'], collection['height'])
                            if ord(character) > 0:
                                characters.append((encode_to_utf8(ord(character)), imgBytes))
                    data.append({'width': collection['width'], 'height': collection['height'], 'ascent': collection['ascent'], 'data': characters})
                
                fout.write((0).to_bytes(4, 'big'))
                for collection in data:
                    fout.write(collection['width'].to_bytes(1, 'big'))
                    fout.write(collection['height'].to_bytes(1, 'big'))
                    fout.write(len(collection['data']).to_bytes(4, 'big'))
                    fout.write(collection['ascent'].to_bytes(1, 'big'))
                    for character in collection['data']:
                        fout.write(character[0])
                    for character in collection['data']:
                        fout.write(character[1])

if __name__ == "__main__":
    main()