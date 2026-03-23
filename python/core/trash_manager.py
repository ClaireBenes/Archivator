from core.resolver  import ProjectResolver

class TrashManager:
    """
    Handles all trash operations.

    Responsibilities:
    - Move files to trash
    - Restore files
    - Empty trash
    - Maintain folder structure
    """

    def __init__(self, resolver: ProjectResolver):
        pass

    def move_to_trash(self, filepath: str):
        """
        Move file to project trash.

        Steps:
        - Resolve project
        - Compute destination path
        - Move file
        """
        pass

    def restore(self, trashed_path: str):
        """Restore file to original location."""
        pass

    def empty_trash(self, project_id: str):
        """Delete all files in trash."""
        pass

    def compute_trash_path(self, project, filepath):
        """Convert original path → trash path"""
        pass