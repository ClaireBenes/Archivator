from core.project import Project
from core.registry import ProjectRegistry

class ProjectResolver:
    """
    Resolves which project a file belongs to.

    Core idea:
    - Input: file path
    - Output: Project
    """

    def __init__(self, registry: ProjectRegistry):
        pass

    def resolve(self, filepath: str) -> Project:
        """
        Find project by matching root path.

        Raises:
            ProjectNotFoundError
        """
        pass