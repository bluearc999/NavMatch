import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QLabel, QHeaderView)
from PyQt5.QtGui import QColor, QDoubleValidator
from database import init_db
from core import verileri_eslestir

class OtomasyonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Navlun - Fatura Otomasyonu")
        self.setGeometry(100, 100, 1000, 600)
        
        self.irsaliye_path = ""
        self.fatura_path = ""
        
        init_db() # Veritabanını başlat
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Dosya Seçim Butonları
        btn_layout = QHBoxLayout()
        
        self.btn_irsaliye = QPushButton("1. Akdeniz İrsaliye Excel'i Seç")
        self.btn_irsaliye.clicked.connect(self.select_irsaliye)
        btn_layout.addWidget(self.btn_irsaliye)
        
        self.btn_fatura = QPushButton("2. Toroslar Fatura Excel'i Seç")
        self.btn_fatura.clicked.connect(self.select_fatura)
        btn_layout.addWidget(self.btn_fatura)

        self.btn_calistir = QPushButton("Karşılaştır ve Eşleştir")
        self.btn_calistir.setStyleSheet("background-color: #2b5b84; color: white; font-weight: bold;")
        self.btn_calistir.clicked.connect(self.islem_baslat)
        btn_layout.addWidget(self.btn_calistir)

        layout.addLayout(btn_layout)

        # Durum Etiketi
        self.lbl_status = QLabel("Lütfen Excel dosyalarını seçin.")
        layout.addWidget(self.lbl_status)

        # Sonuç Tablosu (QTableWidget)
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.tableWidget)

    def select_irsaliye(self):
        path, _ = QFileDialog.getOpenFileName(self, "İrsaliye Excel Seç", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.irsaliye_path = path
            self.btn_irsaliye.setText(f"İrsaliye: {path.split('/')[-1]}")

    def select_fatura(self):
        path, _ = QFileDialog.getOpenFileName(self, "Fatura Excel Seç", "", "Excel Files (*.xlsx *.xls)")
        if path:
            self.fatura_path = path
            self.btn_fatura.setText(f"Fatura: {path.split('/')[-1]}")

    def islem_baslat(self):
        if not self.irsaliye_path or not self.fatura_path:
            QMessageBox.warning(self, "Eksik Dosya", "Lütfen her iki Excel dosyasını da seçin!")
            return

        try:
            # Pandas ile eşleştirme algoritmasını çalıştır
            result_df = verileri_eslestir(self.irsaliye_path, self.fatura_path)
            self.tabloyu_doldur(result_df)
            self.lbl_status.setText(f"İşlem Tamamlandı. Toplam Kayıt: {len(result_df)}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Veri işlenirken hata oluştu:\n{str(e)}")

    def tabloyu_doldur(self, df):
        self.tableWidget.setRowCount(df.shape[0])
        self.tableWidget.setColumnCount(df.shape[1])
        self.tableWidget.setHorizontalHeaderLabels(df.columns)

        for row_idx, row_data in df.iterrows():
            is_error = row_data['Durum'] != "Eşleşti"
            for col_idx, value in enumerate(row_data):
                val_str = str(value) if pd.notna(value) else "-"
                item = QTableWidgetItem(val_str)
                
                # Hatalı/Uyuşmayan satırları KIRMIZI ile vurgulama
                if is_error:
                    item.setBackground(QColor(255, 200, 200)) # Açık Kırmızı
                else:
                    item.setBackground(QColor(200, 255, 200)) # Açık Yeşil
                
                self.tableWidget.setItem(row_idx, col_idx, item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OtomasyonApp()
    window.show()
    sys.exit(app.exec_())
