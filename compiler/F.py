class Chain(object):
    # Thread macro, `->' ripoff from clojure
    def __init__(self, content):
        self._content = content

    def call(self, f, *args):
        args = args + (self._content,)
        self._content = f(*args)
        return self

    def values(self):
        self._content = self._content.values()
        return self

    def flatten(self):
        self._content = reduce(lambda r, x: r + x, self._content, [])
        return self

    def join(self, token):
        self._content = token.join(self._content)
        return self

    def split(self, s):
        self._content = self._content.split(s)
        return self

    def list(self):
        self._content = list(self._content)
        return self

    def map(self, f):
        self._content = map(f, self._content)
        return self

    def filter(self, f):
        self._content = filter(f, self._content)
        return self

    def end(self):
        return self._content


def with_defaults(d, **kwargs):
    for k, v in kwargs.items():
        if k not in d:
            d[k] = v
    return d
