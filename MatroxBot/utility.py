# Holds multi-use utility functions
class Utility:

    def __init__(self):
        self._NUMERALS = '0123456789abcdefABCDEF'
        self._HEXDEC = {v: int(v, 16) for v in (x+y for x in self._NUMERALS for y in self._NUMERALS)}
        self.LOWERCASE = 'x'
        self.UPPERCASE = 'X'
    
    @staticmethod
    def try_parse_int(s, base = 10, value = None):
        try:
            return True, int(s, base)
        except ValueError:
            return False, value

    def hex_to_rgb(self, hexValue):
        rgb = self.rgb(hexValue)
        return rgb

    def rgb(self, triplet):
        return self._HEXDEC[triplet[0:2]], self._HEXDEC[triplet[2:4]], self._HEXDEC[triplet[4:6]]

    def triplet(self, rgb, lettercase='x'):
        return format(rgb[0]<<16 | rgb[1]<<8 | rgb[2], '06'+lettercase)
