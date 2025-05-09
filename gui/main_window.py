import sys
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QTextEdit,
    QMessageBox,
)


class MainWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("SysTraceML")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):

        # Instructions
        self.instructions_btn = QPushButton("Instrucciones")
        self.instructions_btn.clicked.connect(self.show_instructions)

        # Field for input syscalls
        self.input_label = QLabel("Enter syscalls sequence:")
        self.input_field = QTextEdit()

        # Main buttons
        self.predict_btn = QPushButton("Predict")
        self.clear_btn = QPushButton("Clear")
        self.exit_btn = QPushButton("Exit")

        self.predict_btn.clicked.connect(self.predict)
        self.clear_btn.clicked.connect(self.clear_fields)
        self.exit_btn.clicked.connect(self.close)

        # Fields to exit for show the result
        self.result_label = QLabel("Results of the model:")
        self.result_field = QTextEdit()
        self.result_field.setReadOnly(True)

        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.instructions_btn)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_field)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.predict_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.addWidget(self.exit_btn)

        layout.addLayout(btn_layout)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_field)

        self.setLayout(layout)

    def show_instructions(self):
        msg = QMessageBox()
        msg.setWindowTitle("Instructions")
        msg.setText(
            "Enter the syscalls sequence in the text area and click 'Predict' to get the results."
        )
        msg.exec_()

    def predict(self):
        syscalls_input = self.input_field.toPlainText()
        if not syscalls_input:
            self.result_field.setText("Please enter a syscalls sequence.")
            return

        # Here you would call the prediction function from your model
        # For demonstration, we will just echo the input
        resultado = "Normal [Simulated] with 97% confidence"
        self.result_field.setText(resultado)

    def clear_fields(self):
        self.input_field.clear()
        self.result_field.clear()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
