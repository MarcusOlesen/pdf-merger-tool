import sys, os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget,
    QFileDialog, QMessageBox, QListWidgetItem, QProgressDialog, QMenu
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QIcon
from PyPDF2 import PdfMerger


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class PDFMergerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger Tool")
        self.setWindowIcon(QIcon(resource_path("icon.ico")))
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        # --- Buttons ---
        self.select_button = QPushButton("Select PDFs")
        self.select_button.clicked.connect(self.select_pdfs)
        layout.addWidget(self.select_button)

        self.clear_button = QPushButton("Clear All")
        self.clear_button.clicked.connect(self.clear_all)
        layout.addWidget(self.clear_button)

        # --- File List ---
        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.file_list.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.file_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_list.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.file_list)

        # --- Merge Button ---
        self.merge_button = QPushButton("Merge PDFs")
        self.merge_button.clicked.connect(self.merge_pdfs)
        layout.addWidget(self.merge_button)

        self.setLayout(layout)

    # --- Select PDFs ---
    def select_pdfs(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select PDF files",
            "",
            "PDF Files (*.pdf)"
        )
        if files:
            for f in files:
                filename = os.path.basename(f)
                item = QListWidgetItem(filename)
                item.setToolTip(f)
                item.setData(Qt.ItemDataRole.UserRole, f)
                self.file_list.addItem(item)

    # --- Clear all files ---
    def clear_all(self):
        self.file_list.clear()

    # --- Context menu (right-click) for single item ---
    def show_context_menu(self, position: QPoint):
        menu = QMenu()
        remove_action = menu.addAction("Remove Selected File(s)")
        action = menu.exec(self.file_list.viewport().mapToGlobal(position))
        if action == remove_action:
            for item in self.file_list.selectedItems():
                self.file_list.takeItem(self.file_list.row(item))

    # --- Merge PDFs ---
    def merge_pdfs(self):
        count = self.file_list.count()
        if count == 0:
            QMessageBox.warning(self, "No Files", "Please select PDF files first.")
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Merged PDF",
            "merged.pdf",
            "PDF Files (*.pdf)"
        )

        if not save_path:
            return  # User cancelled

        progress = QProgressDialog("Merging PDFs...", None, 0, count, self)
        progress.setWindowTitle("Please wait")
        progress.setWindowModality(Qt.WindowModality.ApplicationModal)
        progress.setCancelButton(None)
        progress.show()

        merger = PdfMerger()
        try:
            for i in range(count):
                pdf_path = self.file_list.item(i).data(Qt.ItemDataRole.UserRole)
                merger.append(pdf_path)
                progress.setValue(i + 1)
                QApplication.processEvents()

            merger.write(save_path)
            merger.close()
            progress.close()

            QMessageBox.information(self, "Success", f"PDFs merged successfully!\nSaved as:\n{save_path}")
            self.close()
        except Exception as e:
            progress.close()
            QMessageBox.critical(self, "Error", f"An error occurred:\n{e}")


def main():
    app = QApplication(sys.argv)
    window = PDFMergerApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
