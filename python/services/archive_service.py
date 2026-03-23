class ArchiveService:
    """
    High-level API used by:
    - CLI
    - UI
    - External tools (Prism plugin)

    This is the MAIN ENTRY POINT.
    """

    def move_to_trash(self, filepath: str):
        """
        Resolve project → move file
        """
        pass

    def restore(self, filepath: str):
        pass

    def empty_project_trash(self, project_id: str):
        pass

    def add_project(self, root_path: str, trash_dir: str):
        pass

    def list_projects(self):
        pass