import io
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, 
                              QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, 
                              QMessageBox, QProgressBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage
from PIL import Image
from rembg import remove

class RemovedorDeFundoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Removedor de Fundo de Imagem")
        self.setMinimumSize(800, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333333;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title = QLabel("Removedor de Fundo de Imagem")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
            margin: 20px;
        """)
        layout.addWidget(title)
        
        # Área de preview
        self.preview_frame = QWidget()
        self.preview_frame.setStyleSheet("""
            QWidget {
                background-color: gray;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                min-height: 400px;
            }
        """)
        preview_layout = QVBoxLayout(self.preview_frame)
        
        self.preview_label = QLabel("Clique em 'Selecionar Imagem'")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("""
            font-size: 14px;
            font-style: italic;
            color: #666666;
        """)
        preview_layout.addWidget(self.preview_label)
        
        layout.addWidget(self.preview_frame)
        
        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2196F3;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Container de botões
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)
        
        # Botões
        self.btn_abrir = QPushButton("Selecionar Imagem")
        self.btn_abrir.clicked.connect(self.selecionar_imagem)
        self.btn_abrir.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        
        self.btn_salvar = QPushButton("Salvar Imagem sem Fundo")
        self.btn_salvar.clicked.connect(self.salvar_imagem)
        self.btn_salvar.setEnabled(False)
        self.btn_salvar.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.btn_abrir)
        button_layout.addWidget(self.btn_salvar)
        button_layout.addStretch()
        
        layout.addWidget(button_container)
        
        # Status bar
        self.statusBar().showMessage("Pronto para processar")
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: #f5f5f5;
                color: #666666;
                padding: 5px;
                font-size: 12px;
            }
        """)
        
        self.imagem_resultado = None
        self.show()

    def selecionar_imagem(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar Imagem",
            "",
            "Imagens (*.png *.jpg *.jpeg)"
        )
        
        if file_name:
            try:
                self.statusBar().showMessage("Processando imagem...")
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(30)
                QApplication.processEvents()
                
                with open(file_name, 'rb') as img_file:
                    imagem_bytes = img_file.read()
                
                self.progress_bar.setValue(60)
                QApplication.processEvents()
                
                imagem_sem_fundo = remove(imagem_bytes)
                self.imagem_resultado = Image.open(io.BytesIO(imagem_sem_fundo))
                
                # Converter PIL Image para QPixmap
                img_qt = self.pil_to_pixmap(self.imagem_resultado)
                
                # Redimensionar mantendo proporção
                scaled_pixmap = img_qt.scaled(
                    self.preview_frame.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                
                self.preview_label.setPixmap(scaled_pixmap)
                self.btn_salvar.setEnabled(True)
                
                self.progress_bar.setValue(100)
                self.statusBar().showMessage("Fundo removido com sucesso!")
                
            except Exception as e:
                self.statusBar().showMessage("Erro ao processar imagem")
                QMessageBox.critical(self, "Erro", f"Ocorreu um erro ao remover o fundo:\n{str(e)}")
            
            finally:
                self.progress_bar.setVisible(False)

    def salvar_imagem(self):
        if self.imagem_resultado is None:
            return
            
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Imagem",
            "",
            "PNG (*.png)"
        )
        
        if file_name:
            try:
                self.statusBar().showMessage("Salvando imagem...")
                self.imagem_resultado.save(file_name, "PNG")
                self.statusBar().showMessage("Imagem salva com sucesso!")
                
            except Exception as e:
                self.statusBar().showMessage("Erro ao salvar imagem")
                QMessageBox.critical(self, "Erro", f"Erro ao salvar a imagem:\n{str(e)}")

    def pil_to_pixmap(self, pil_image):
        # Converter PIL Image para QPixmap
        if pil_image.mode == "RGBA":
            qimage = QImage(
                pil_image.tobytes('raw', 'RGBA'),
                pil_image.size[0],
                pil_image.size[1],
                QImage.Format_RGBA8888
            )
        else:
            pil_image = pil_image.convert("RGBA")
            qimage = QImage(
                pil_image.tobytes('raw', 'RGBA'),
                pil_image.size[0],
                pil_image.size[1],
                QImage.Format_RGBA8888
            )
        return QPixmap.fromImage(qimage)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Configurar estilo global da aplicação
    app.setStyle('Fusion')
    
    ex = RemovedorDeFundoApp()
    sys.exit(app.exec())