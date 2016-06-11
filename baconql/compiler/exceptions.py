class InvalidHeaderException(Exception):
    pass


class UnknownMappingException(Exception):
    pass


class InvalidDefinitionException(Exception):
    pass


class LoadingException(Exception):
    def __init__(self, reason, file_path, line):
        super(LoadingException, self).__init__(
            "%s for file: `%s' at line %d" % (reason, file_path, line))
