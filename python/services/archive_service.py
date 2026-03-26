import os
import uuid

from core.project import Project
from core.registry import ProjectRegistry
from core.resolver import ProjectResolver
from core.trash_manager import TrashManager
from core.exceptions import InvalidProjectError


class ArchiveService:
    """
    High-level API used by:
    - CLI
    - UI
    - External tools (Prism plugin)

    This is the MAIN ENTRY POINT.
    """

    def __init__(self, registry: ProjectRegistry):
        """
        Initialize the ArchiveService.

        Args:
            registry (ProjectRegistry): Project registry instance.
        """

        self.registry = registry
        self.resolver = ProjectResolver(registry)
        self.trash_manager = TrashManager(self.resolver)

    def move_to_trash(self, filepath: str) -> str:
        """
        Move a file to its project's trash.

        Args:
            filepath (str): Path to the file.

        Returns:
            str: Destination path in trash.
        """

        return self.trash_manager.move_to_trash(filepath)

    def restore(self, filepath: str) -> str:
        """
        Restore a file from trash.

        Args:
            filepath (str): Path to the file in trash.

        Returns:
            str: Restored file path.
        """

        return self.trash_manager.restore(filepath)

    def empty_project_trash(self, project_id: str) -> None:
        """
        Empty the trash for a given project.

        Args:
            project_id (str): ID of the project.
        """

        self.trash_manager.empty_trash(project_id)

    def add_project(self, root_path: str, trash_dir: str) -> Project:
        """
        Create and register a new project.

        Args:
            root_path (str): Root directory of the project.
            trash_dir (str): Trash directory for the project.

        Returns:
            Project: The created project.

        Raises:
            InvalidProjectError: If paths are invalid.
        """

        # Validate root path
        if not os.path.exists(root_path):
            raise InvalidProjectError(f"Root path does not exist: {root_path}")

        # Generate unique ID
        project_id = str(uuid.uuid4())

        # Use folder name as default project name
        name = os.path.basename(os.path.abspath(root_path))

        # Default config (can be expanded later)
        collect_config = {}
        paths = []

        project = Project(
            id=project_id,
            name=name,
            root=root_path,
            trash_dir=trash_dir,
            collect_config=collect_config,
            paths=paths,
        )

        # Add to registry (includes validation + save)
        self.registry.add_project(project)
        self.registry.save()

        return project

    def list_projects(self) -> list:
        """
        Get all registered projects.

        Returns:
            list[Project]: List of projects.
        """

        return self.registry.get_all()