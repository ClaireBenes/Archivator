class ArchivatorError(Exception):
    pass

class ProjectNotFoundError(ArchivatorError):
    pass

class InvalidProjectError(ArchivatorError):
    pass