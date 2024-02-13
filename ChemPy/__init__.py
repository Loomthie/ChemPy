class HTMLDict(dict):
    def __missing__(self, key):
        return f"{{{key}}}"
