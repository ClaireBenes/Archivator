import os

class Project:
    """
    Represents a single project.

    Holds:
    - id
    - name
    - root path
    - trash directory
    - collection settings
    - list of managed subpaths
    """

    def __init__(self, id, name, root, trash_dir, collect_config, paths):
        pass

    def is_path_inside(self, filepath: str) -> bool:
        pass