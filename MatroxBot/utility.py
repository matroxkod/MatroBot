# Holds multi-use utility functions
class Utility:

    
    @staticmethod
    def try_parse_int(s, base = 10, value = None):
        try:
            return True, int(s, base)
        except ValueError:
            return False, value