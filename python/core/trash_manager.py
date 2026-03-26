import os
import shutil

from core.resolver import ProjectResolver
from core.exceptions import ArchivatorError

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
        """
        Initialize the TrashManager.

        Args:
            resolver (ProjectResolver): Resolver used to determine project from file paths.
        """
        self.resolver = resolver


    def move_to_trash(self, filepath: str) -> str:
        """
        Move a file and all related files with the same base name to the project's trash.

        Keeps the project structure and avoids overwriting existing files.

        Args:
            filepath (str): Path to the main file to move.

        Returns:
            str: Destination path of the main file in trash.

        Raises:
            FileNotFoundError: If the file does not exist.
            ArchivatorError: If moving fails.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File does not exist: {filepath}")

        # Resolve project using your existing resolver
        project = self.resolver.resolve(filepath)

        folder = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        base_name, ext = os.path.splitext(filename)

        main_dest_path = None

        # Move all files in the folder with the same base name
        for f in os.listdir(folder):
            if f.startswith(base_name):
                src = os.path.join(folder, f)
                # Compute trash path relative to project
                rel_path = os.path.relpath(src, project.root)
                dest = os.path.join(project.trash_dir, rel_path)

                # Ensure destination folder exists
                os.makedirs(os.path.dirname(dest), exist_ok=True)

                # Avoid overwriting in trash
                counter = 1
                orig_dest = dest
                while os.path.exists(dest):
                    name, ext2 = os.path.splitext(os.path.basename(orig_dest))
                    parent = os.path.dirname(orig_dest)
                    dest = os.path.join(parent, f"{name}_{counter}{ext2}")
                    counter += 1

                shutil.move(src, dest)

                if f == filename:
                    main_dest_path = dest

        if main_dest_path is None:
            raise ArchivatorError(f"Failed to move main file '{filepath}' to trash.")

        return main_dest_path

    def restore(self, trashed_path: str) -> str:
        """
        Restore a file from trash to its original location.

        Args:
            trashed_path (str): Path to the file inside the trash.

        Returns:
            str: Restored file path.

        Raises:
            FileNotFoundError: If the trashed file does not exist.
        """

        if not os.path.exists(trashed_path):
            raise FileNotFoundError(f"File does not exist: {trashed_path}")

        # Resolve project from trash path
        project = self.resolver.resolve(trashed_path)

        # Compute original path by reversing trash structure
        relative_path = os.path.relpath(trashed_path, project.trash_dir)
        original_path = os.path.join(project.root, relative_path)

        # Ensure original directory exists
        os.makedirs(os.path.dirname(original_path), exist_ok=True)

        # Move file back
        shutil.move(trashed_path, original_path)

        return original_path

    def empty_trash(self, project_id: str):
        """
        Delete all files inside a project's trash directory.

        Args:
            project_id (str): ID of the project.
        """

        # Get project via resolver's registry
        project = self.resolver.registry.find_by_id(project_id)

        if not os.path.exists(project.trash_dir):
            return

        # Remove entire trash directory
        shutil.rmtree(project.trash_dir)

        # Recreate empty trash folder
        os.makedirs(project.trash_dir, exist_ok=True)

    def compute_trash_path(self, project, filepath) -> str:
        """
        Compute the destination path in the trash.

        The original folder structure is preserved inside the trash directory.

        Args:
            project (Project): Project instance.
            filepath (str): Original file path.

        Returns:
            str: Destination path inside trash.
        """

        # Get path relative to project root
        relative_path = os.path.relpath(filepath, project.root)

        # Rebuild path inside trash
        trash_path = os.path.join(project.trash_dir, relative_path)

        return trash_path