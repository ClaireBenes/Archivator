import os

class Project:
    """
    Represents a single project.

    Holds:
    - id: unique identifier (string)
    - name: human-readable name
    - root: absolute path to project root directory
    - trash_dir: absolute path to trash directory
    - collect_config: dict containing collection rules/settings
    - paths: list of subdirectories (relative to root) to scan
    """

    def __init__(self, id, name, root, trash_dir, collect_config, paths):
        """
        Initialize a Project instance.

        Args:
            id (str): Unique project identifier
            name (str): Project name
            root (str): Root directory of the project
            trash_dir (str): Directory where deleted files are stored
            collect_config (dict): Cleanup/collection configuration
            paths (list[str]): Subdirectories to scan (relative to root)
        """

        # Store basic info
        self.id = id
        self.name = name

        # Normalize paths to avoid inconsistencies
        self.root = os.path.abspath(root)
        self.trash_dir = os.path.abspath(trash_dir)

        # Store config and Ensure we always have usable defaults
        self.collect_config = collect_config or {}
        self.paths = paths or []

    def is_path_inside(self, filepath: str) -> bool:
        """
        Check whether a given file path belongs to this project.

        Args:
            filepath (str): Path to the file to check.

        Returns:
            bool: True if the file is inside the project root directory,
                  False otherwise.
        """

        # Normalize the input path
        filepath = os.path.abspath(filepath)

        try:
            # Get the common base path between the file and project root
            common_path = os.path.commonpath([filepath, self.root])

            # If they share the same root, the file belongs to the project
            return common_path == self.root

        except ValueError:
            # Happens if paths are on different drives (mostly Windows)
            return False