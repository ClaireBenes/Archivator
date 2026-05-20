import os

class ProjectDropHelper:
    """
    Handle project folder drag/drop on the project cards area.
    """

    def __init__(self, main_window) -> None:
        self.main_window = main_window

    def on_project_drag_enter(self, event) -> None:
        if self.get_first_dropped_folder(event):
            event.acceptProposedAction()
            self.set_drag_feedback(True)
        else:
            event.ignore()

    def on_project_drag_leave(self, event) -> None:
        self.set_drag_feedback(False)
        event.accept()

    def on_project_drop(self, event) -> None:
        folder = self.get_first_dropped_folder(event)
        self.set_drag_feedback(False)

        if not folder:
            event.ignore()
            return

        event.acceptProposedAction()
        self.main_window.add_project(root_path=folder)

    def get_first_dropped_folder(self, event) -> str | None:
        mime_data = event.mimeData()

        if not mime_data.hasUrls():
            return None

        for url in mime_data.urls():
            path = url.toLocalFile()

            if path and os.path.isdir(path):
                return path.replace("\\", "/")

        return None

    def set_drag_feedback(self, active: bool) -> None:
        cards_widget = self.main_window.cards_widget
        cards_widget.setProperty("dragActive", active)

        for card in self.main_window.project_cards:
            card.set_dimmed(active)

        cards_widget.style().unpolish(cards_widget)
        cards_widget.style().polish(cards_widget)