import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import *

from core.exceptions import ArchivatorError
from core.registry import ProjectRegistry
from services.archive_service import ArchiveService

from ui.dialogs.add_project_dialog import AddProjectDialog
from ui.layouts.flow_layout import FlowLayout
from ui.widgets.add_project_card import AddProjectCard
from ui.widgets.project_card import ProjectCard

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class MainWindow:
    """
    Main UI controller.

    Responsibilities:
    - Load the .ui file
    - Bind UI widgets
    - Display project cards
    - Forward user actions to ArchiveService
    """

    def __init__(self) -> None:
        self.ui_path = ROOT / "ui" / "view" / "interface.ui"
        self.config_path = ROOT / "config" / "projects.json"
        self.data_path = ROOT.parent / "data"
        self.placeholder_path = self.data_path / "placeholder.png"

        self.registry = ProjectRegistry(str(self.config_path))
        self.registry.load()
        self.service = ArchiveService(self.registry)

        self.window = self.load_ui()
        self.bind_widgets()
        self.setup_project_area()
        self.connect_signals()
        self.refresh_projects()

    def load_ui(self):
        """
        Load the main window from the Qt Designer .ui file.
        """
        loader = QUiLoader()
        window = loader.load(str(self.ui_path))

        if window is None:
            raise RuntimeError(f"Could not load UI: {self.ui_path}")

        return window

    def bind_widgets(self) -> None:
        """
        Retrieve important widgets from the loaded UI.
        """
        self.project_container = self.window.findChild(QWidget, "projectContainer")
        self.search_bar = self.window.findChild(QLineEdit, "searchLineEdit")
        self.settings_button = self.window.findChild(QPushButton, "settingsButton")
        self.sort_combo = self.window.findChild(QComboBox, "sortComboBox")
        self.stats_label = self.window.findChild(QLabel, "statsLabel")

        if self.project_container is None:
            raise RuntimeError("Missing widget 'projectContainer' in interface.ui")

    def setup_project_area(self) -> None:
        """
        Create the scroll area and flow layout used for project cards.
        """
        old_layout = self.project_container.layout()
        if old_layout is not None:
            QWidget().setLayout(old_layout)

        outer_layout = QVBoxLayout(self.project_container)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(QFrame.NoFrame)

        self.cards_widget = QWidget()
        self.flow_layout = FlowLayout(self.cards_widget, margin=0, hspacing=24, vspacing=24)
        self.cards_widget.setLayout(self.flow_layout)

        self.scroll_area.setWidget(self.cards_widget)
        outer_layout.addWidget(self.scroll_area)

    def connect_signals(self) -> None:
        """
        Connect UI events.
        """
        if self.search_bar is not None:
            self.search_bar.textChanged.connect(self.refresh_projects)

        if self.sort_combo is not None:
            self.sort_combo.currentIndexChanged.connect(self.refresh_projects)

    def clear_cards(self) -> None:
        """
        Remove all cards from the project area.
        """
        while self.flow_layout.count():
            item = self.flow_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def refresh_projects(self) -> None:
        """
        Reload and display the visible project cards.
        """
        self.clear_cards()

        projects = self.service.list_projects()
        projects = self.filter_projects(projects)
        projects = self.sort_projects(projects)

        if self.stats_label is not None:
            self.stats_label.setText(f"{len(projects)} projects registered")

        self.flow_layout.addWidget(AddProjectCard(self.add_project))

        for project in projects:
            self.flow_layout.addWidget(ProjectCard(project, self, str(self.placeholder_path)))

    def filter_projects(self, projects: list) -> list:
        """
        Filter projects according to the search bar.
        """
        if self.search_bar is None:
            return projects

        search_text = self.search_bar.text().strip().lower()
        if not search_text:
            return projects

        return [
            project for project in projects
            if search_text in project.name.lower()
        ]

    def sort_projects(self, projects: list) -> list:
        """
        Sort projects according to the combo box selection.
        """
        if self.sort_combo is None:
            return projects

        current_text = self.sort_combo.currentText()

        if "Name" in current_text:
            return sorted(projects, key=lambda p: p.name.lower())

        if "Path" in current_text:
            return sorted(projects, key=lambda p: p.root.lower())

        return projects

    def add_project(self) -> None:
        dialog = AddProjectDialog(self.window)

        if dialog.exec() != QDialog.Accepted:
            return

        root_path, trash_dir = dialog.get_values()

        try:
            self.service.add_project(root_path, trash_dir)
            self.refresh_projects()

        except ArchivatorError as exc:
            QMessageBox.warning(self.window, "Archivator Error", str(exc))
        except Exception as exc:
            QMessageBox.critical(self.window, "Unexpected Error", str(exc))

    def open_project(self, project) -> None:
        """
        Ask the service to open the selected project's root folder.
        """
        try:
            self.service.open_project_root(project.id)
        except Exception as exc:
            QMessageBox.critical(self.window, "Error", str(exc))

    def open_project_trash(self, project) -> None:
        """
        Ask the service to open the selected project's trash folder.
        """
        try:
            self.service.open_project_trash(project.id)
        except Exception as exc:
            QMessageBox.critical(self.window, "Error", str(exc))

    def empty_project_trash(self, project) -> None:
        """
        Empty the trash directory for the selected project.
        """
        reply = QMessageBox.question(
            self.window,
            "Confirm",
            f"Empty trash for\n{project.name} ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            self.service.empty_project_trash(project.id)
            QMessageBox.information(self.window, "Done", "Trash emptied.")
        except ArchivatorError as exc:
            QMessageBox.warning(self.window, "Archivator Error", str(exc))
        except Exception as exc:
            QMessageBox.critical(self.window, "Unexpected Error", str(exc))

    def open_project_settings(self, project) -> None:
        """
        Display project settings information.
        """
        QMessageBox.information(
            self.window,
            "Project Settings",
            f"Here you can later edit settings for:\n\n"
            f"{project.name}\n\n"
            f"Root: {project.root}\n"
            f"Trash: {project.trash_dir}",
        )

    def remove_project(self, project) -> None:
        """
        Remove a project from the registry after user confirmation.
        """
        reply = QMessageBox.question(
            self.window,
            "Remove Project",
            f"Remove '{project.name}' from Archivator?\n\n"
            f"This will only unregister the project.\n"
            f"No files or folders will be deleted.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            self.service.remove_project(project.id)
            self.refresh_projects()
            QMessageBox.information(
                self.window,
                "Project Removed",
                f"Project removed:\n\n{project.name}",
            )
        except ArchivatorError as exc:
            QMessageBox.warning(self.window, "Archivator Error", str(exc))
        except Exception as exc:
            QMessageBox.critical(self.window, "Unexpected Error", str(exc))

    def show(self) -> None:
        """
        Show the main window.
        """
        self.window.show()