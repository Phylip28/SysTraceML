import sys
import joblib
from collections import Counter
import os
import pandas as pd

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

        # Load model
        model_path = os.path.join("models", "model.pkl")
        self.model = joblib.load(model_path)

        # Load syscalls used during training
        self.syscalls_ids = list(range(0, 450))

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

        syscalls_input = self.input_field.toPlainText().strip()

        if not syscalls_input:
            self.result_field.setText("Please enter a syscalls sequence.")
            return

        try:
            # Verifica que todos los elementos sean números
            syscall_str_list = syscalls_input.split()
            syscall_list = [int(x) for x in syscall_str_list]

            # Contar frecuencia de cada syscall_id
            freq_counter = Counter(syscall_list)

            # Crear vector de características con todas las posibles syscall_ids
            feature_vector = [freq_counter.get(i, 0) for i in self.syscalls_ids]

            # Convertir a DataFrame (con nombres de columnas si es necesario)
            input_df = pd.DataFrame([feature_vector], columns=self.syscalls_ids)

            # Predicción
            prediction = self.model.predict(input_df)[0]
            proba = self.model.predict_proba(input_df)[0]
            confidence = max(proba) * 100

            label = "Normal" if prediction == 0 else "Attack"
            self.result_field.setText(f"{label} ({confidence:.2f}% confidence)")

        except ValueError as ve:
            self.result_field.setText(
                f"Invalid input. Ensure only integers separated by spaces.\nError: {ve}"
            )

        except Exception as e:
            self.result_field.setText(f"Unexpected error: {e}")

    def clear_fields(self):

        self.input_field.clear()
        self.result_field.clear()


def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


main()
