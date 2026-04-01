import os
import uuid
from typing import List

from core.project import Project
from core.registry import ProjectRegistry
from core.resolver import ProjectResolver
from core.trash_manager import TrashManager
from core.exceptions import InvalidProjectError

from services.desktop_service import DesktopService


class ArchiveService:
    """
    High-level API used by:
    - CLI
    - UI
    - External tools (Prism plugin)

    This is the main application entry point.
    """

    def __init__(self, registry: ProjectRegistry):
        """
        Initialize the archive service.

        Args:
            registry (ProjectRegistry): Project registry instance.
        """
        self.registry = registry
        self.resolver = ProjectResolver(registry)
        self.trash_manager = TrashManager(self.resolver)
        self.desktop_service = DesktopService()

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
        if not os.path.exists(root_path):
            raise InvalidProjectError(f"Root path does not exist: {root_path}")

        project_id = str(uuid.uuid4())
        name = os.path.basename(os.path.abspath(root_path))
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

        self.registry.add_project(project)
        self.registry.save()

        return project

    def list_projects(self) -> List[Project]:
        """
        Get all registered projects.

        Returns:
            List[Project]: List of registered projects.
        """
        return self.registry.get_all()

    def get_project(self, project_id: str) -> Project:
        """
        Get a project by its ID.

        Args:
            project_id (str): Project ID.

        Returns:
            Project: Matching project.
        """
        return self.registry.find_by_id(project_id)

    def get_project_from_path(self, filepath: str) -> Project:
        """
        Resolve and return the project owning a given path.

        Args:
            filepath (str): A path inside the project.

        Returns:
            Project: Matching project.
        """
        return self.resolver.resolve(filepath)

    def open_project_root(self, project_id: str) -> None:
        """
        Open a project's root folder in the system file browser.

        Args:
            project_id (str): Project ID.
        """
        project = self.registry.find_by_id(project_id)
        self.desktop_service.open_folder(project.root)

    def open_project_root_from_path(self, filepath: str) -> None:
        """
        Resolve the project from a path and open its root folder.

        Args:
            filepath (str): A path inside the project.
        """
        project = self.resolver.resolve(filepath)
        self.desktop_service.open_folder(project.root)

    def open_project_trash(self, project_id: str) -> None:
        """
        Open a project's trash folder in the system file browser.

        Args:
            project_id (str): Project ID.
        """
        project = self.registry.find_by_id(project_id)
        self.desktop_service.open_folder(project.trash_dir)

    def open_trash_from_path(self, filepath: str) -> None:
        """
        Resolve the project from a path and open its trash folder.

        Args:
            filepath (str): A path inside the project.
        """
        project = self.resolver.resolve(filepath)

        if not os.path.exists(project.trash_dir):
            os.makedirs(project.trash_dir, exist_ok=True)

        self.desktop_service.open_folder(project.trash_dir)