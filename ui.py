import sys
from PyQt5.QtGui import QTextCharFormat, QColor
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QVBoxLayout, QPushButton, QWidget, QLabel, QComboBox, QMessageBox, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("String Matching and Replacement Tool")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Top layout for controls
        top_layout = QHBoxLayout()
        self.algorithm_selector = QComboBox()
        self.algorithm_selector.addItems(["Rabin-Karp", "KMP"])
        top_layout.addWidget(self.algorithm_selector)

        self.search_button = QPushButton("Search Pattern")
        self.search_button.clicked.connect(self.search_algorithm)
        top_layout.addWidget(self.search_button)

        self.replace_button = QPushButton("Replace Current")
        self.replace_button.clicked.connect(self.replace_pattern)
        top_layout.addWidget(self.replace_button)

        self.replace_all_button = QPushButton("Replace All")
        self.replace_all_button.clicked.connect(self.replace_all_patterns)
        top_layout.addWidget(self.replace_all_button)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(self.prev_result)
        top_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(self.next_result)
        top_layout.addWidget(self.next_button)

        self.layout.addLayout(top_layout)

        # Pattern input
        self.label_pattern = QLabel("Enter Pattern:")
        self.layout.addWidget(self.label_pattern)
        self.pattern_edit = QTextEdit()
        self.pattern_edit.setFixedHeight(50)
        self.layout.addWidget(self.pattern_edit)

        # Text input
        self.label_text = QLabel("Enter Text:")
        self.layout.addWidget(self.label_text)
        self.text_edit = QTextEdit()
        self.text_edit.setFixedHeight(300)
        self.layout.addWidget(self.text_edit)

        # Replacement text field
        self.label_replace = QLabel("Replace With:")
        self.layout.addWidget(self.label_replace)
        self.replace_edit = QLineEdit()
        self.layout.addWidget(self.replace_edit)

        # Word count display
        self.word_count_label = QLabel("Word Count: 0")
        self.layout.addWidget(self.word_count_label)

        # Initialize current index and results
        self.current_index = -1
        self.results = []

    def search_algorithm(self):
        self.results.clear()
        text = self.text_edit.toPlainText()
        pattern = self.pattern_edit.toPlainText()

        if not text or not pattern or self.algorithm_selector.currentIndex() == -1:
            QMessageBox.warning(self, "Input Error", "Please enter both text and pattern and select an algorithm.")
            return

        selected_algorithm = self.algorithm_selector.currentText()
        from algorithms import StringMatchingAlgorithms

        if selected_algorithm == "Rabin-Karp":
            self.results = StringMatchingAlgorithms.rabin_karp(pattern, text)
        elif selected_algorithm == "KMP":
            self.results = StringMatchingAlgorithms.KMPSearch(pattern, text)

        word_count = len(text.split())
        self.word_count_label.setText(f"Word Count: {word_count}")

        if not self.results:
            QMessageBox.information(self, "Results", "Pattern not found.")
            return

        self.highlight_results(pattern)

    def highlight_results(self, pattern):
        cursor = self.text_edit.textCursor()
        cursor.select(cursor.Document)
        cursor.setCharFormat(QTextCharFormat())  # Clear previous highlights

        for start in self.results:
            cursor.setPosition(start)
            cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(pattern))
            format = QTextCharFormat()
            format.setBackground(QColor(200, 200, 200))  # Light gray for other matches
            cursor.mergeCharFormat(format)

        cursor.clearSelection()
        if self.results:
            self.current_index = -1

    def replace_pattern(self):
        text = self.text_edit.toPlainText()
        pattern = self.pattern_edit.toPlainText()
        replacement = self.replace_edit.text()

        if pattern in text:
            if self.current_index != -1:
                start_index = self.results[self.current_index]
                end_index = start_index + len(pattern)

                # Replace the pattern at the current index
                new_text = text[:start_index] + replacement + text[end_index:]
                self.text_edit.setPlainText(new_text)

                QMessageBox.information(self, "Replace", f"Replaced '{pattern}' with '{replacement}'.")

                # Update the results after replacement
                selected_algorithm = self.algorithm_selector.currentText()
                from algorithms import StringMatchingAlgorithms

                if selected_algorithm == "Rabin-Karp":
                    self.results = StringMatchingAlgorithms.rabin_karp(pattern, new_text)
                elif selected_algorithm == "KMP":
                    self.results = StringMatchingAlgorithms.KMPSearch(pattern, new_text)

                word_count = len(new_text.split())
                self.word_count_label.setText(f"Word Count: {word_count}")

                # Highlight the new result
                self.highlight_results(pattern)
            else:
                QMessageBox.warning(self, "Replace Error", "No current result to replace.")
        else:
            QMessageBox.warning(self, "Replace Error", f"Pattern '{pattern}' not found for replacement.")



    def replace_all_patterns(self):
        text = self.text_edit.toPlainText()
        pattern = self.pattern_edit.toPlainText()
        replacement = self.replace_edit.text()

        if pattern in text:
            new_text = text.replace(pattern, replacement)
            self.text_edit.setPlainText(new_text)
            replacements = text.count(pattern)
            QMessageBox.information(self, "Replace All", f"Replaced {replacements} occurrences of '{pattern}' with '{replacement}'.")

            word_count = len(new_text.split())
            self.word_count_label.setText(f"Word Count: {word_count}")

            self.search_algorithm()
        else:
            QMessageBox.warning(self, "Replace All Error", f"Pattern '{pattern}' not found for replacement.")

    def prev_result(self):
        if not self.results:
            QMessageBox.warning(self, "Navigation Error", "No results to navigate.")
            return

        self.current_index = (self.current_index - 1) % len(self.results)
        self.highlight_current_result()

    def next_result(self):
        if not self.results:
            QMessageBox.warning(self, "Navigation Error", "No results to navigate.")
            return

        self.current_index = (self.current_index + 1) % len(self.results)
        self.highlight_current_result()

    def highlight_current_result(self):
        cursor = self.text_edit.textCursor()
        pattern = self.pattern_edit.toPlainText()

        if self.results and 0 <= self.current_index < len(self.results):
            cursor.select(cursor.Document)
            cursor.setCharFormat(QTextCharFormat())

            for i in range(len(self.results)):
                cursor.setPosition(self.results[i])
                cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(pattern))
                format = QTextCharFormat()
                format.setBackground(QColor(200, 200, 200))
                cursor.mergeCharFormat(format)

            cursor.setPosition(self.results[self.current_index])
            cursor.movePosition(cursor.Right, cursor.KeepAnchor, len(pattern))
            highlight_format = QTextCharFormat()
            highlight_format.setBackground(QColor(255, 255, 102))
            cursor.mergeCharFormat(highlight_format)
