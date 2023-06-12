# My binary font converter

There's two fonts Minecraft's and the unifont (current version 15.0.05)

## File format

`version:uint32_t` (`character-width:uint8_t` `character-height:uint8_t` `characters-count:uint32_t` `ascent:uint8_t` `characters:utf8[characters-count]` `glyphs:uint8_t[character-bytes * characters-count]`) - repeat until EOF

### Additional info for file format:

* `character-pixels:uint32_t = character-width*character-height`
* `character-bytes:uint32_t = character-pixels // 8 + (1 if (character-pixels % 8 > 0) else 0)`
* `ascent` - how many pixels the glyph should be raised above the base line