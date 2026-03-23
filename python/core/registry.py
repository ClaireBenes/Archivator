from core.project import Project

class ProjectRegistry:
    """
    Single source of truth for all projects.

    Responsibilities:
    - Load/save JSON config
    - Add/remove/update projects
    - Ensure no duplicate roots or trash dirs
    """

    def load(self):
        """Load projects from JSON."""
        pass

    def save(self):
        """Persist projects to disk."""
        pass

    def add_project(self, project: Project):
        pass

    def get_all(self) -> list:
        pass

    def find_by_id(self, project_id: str) -> Project:
        pass