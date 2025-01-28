import os
import platform
import subprocess
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QMessageBox, QGridLayout, QListWidget, QFileDialog, QDialog, QMenuBar, QMenu, QColorDialog, QFrame, QLineEdit, QTextEdit, QComboBox
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor, QPainter, QPen
from PyQt5.QtCore import Qt, QUrl, QPropertyAnimation, QRect, QTimer, QTime
from PyQt5.QtWebEngineWidgets import QWebEngineView  # Web tarayıcısı için gerekli

class AnalogClock(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)  # Saat boyutu
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)  # Her saniye güncelle

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Saat çerçevesi
        painter.setPen(QPen(Qt.black, 8))
        painter.drawEllipse(10, 10, 180, 180)  # Dış çerçeve

        # Saat dilimleri
        current_time = QTime.currentTime()
        hour = current_time.hour() % 12
        minute = current_time.minute()
        second = current_time.second()

        # Saatin açısını hesapla
        hour_angle = (hour + minute / 60) * 30  # 360/12 = 30 derece
        minute_angle = (minute + second / 60) * 6  # 360/60 = 6 derece
        second_angle = second * 6  # 360/60 = 6 derece

        # Saat, dakika ve saniye iğneleri
        self.draw_hand(painter, hour_angle, 50, 8)  # Saat iğnesi
        self.draw_hand(painter, minute_angle, 70, 6)  # Dakika iğnesi
        self.draw_hand(painter, second_angle, 90, 2, Qt.red)  # Saniye iğnesi

    def draw_hand(self, painter, angle, length, width, color=Qt.black):
        painter.setPen(QPen(color, width))
        painter.save()
        painter.translate(100, 100)  # Merkez
        painter.rotate(angle)  # Açıyı döndür
        painter.drawLine(0, 0, 0, -length)  # İğneyi çiz
        painter.restore()

class SimpleOS(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Masaüstü Ortamı 🍐")  # Armut emojisi eklendi
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #F0F0F0;")  # Varsayılan arka plan rengi

        self.initUI()

    def initUI(self):
        # Menü çubuğu
        menubar = self.menuBar()
        start_menu = QMenu("Başlat 🍐", self)  # Armut emojisi eklendi
        menubar.addMenu(start_menu)

        # Menü öğeleri
        open_file_manager_action = start_menu.addAction("📁 Dosya Yöneticisi")
        open_file_manager_action.triggered.connect(self.open_file_manager)

        open_settings_action = start_menu.addAction("⚙️ Ayarlar")
        open_settings_action.triggered.connect(self.open_settings)

        open_system_info_action = start_menu.addAction("ℹ️ Sistem Bilgileri")
        open_system_info_action.triggered.connect(self.open_system_info)

        open_browser_action = start_menu.addAction("🌐 Tarayıcı")
        open_browser_action.triggered.connect(self.open_browser)

        open_notepad_action = start_menu.addAction("📝 Kendi Not Defterimiz")
        open_notepad_action.triggered.connect(self.open_custom_notepad)

        open_calculator_action = start_menu.addAction("🧮 Kendi Hesap Makinemiz")
        open_calculator_action.triggered.connect(self.open_custom_calculator)

        # Mayın Tarlası Oyunu
        open_minesweeper_action = start_menu.addAction("💣 Mayın Tarlası")
        open_minesweeper_action.triggered.connect(self.open_minesweeper)

        # Kullanım Kılavuzu
        open_guide_action = start_menu.addAction("📚 Kullanım Kılavuzu")
        open_guide_action.triggered.connect(self.open_guide)

        # Web uygulamaları
        open_google_action = start_menu.addAction("🔍 Google")
        open_google_action.triggered.connect(lambda: self.open_web_app("https://www.google.com"))

        open_youtube_action = start_menu.addAction("📺 YouTube")
        open_youtube_action.triggered.connect(lambda: self.open_web_app("https://www.youtube.com"))

        open_github_action = start_menu.addAction("🐱 GitHub")
        open_github_action.triggered.connect(lambda: self.open_web_app("https://www.github.com"))

        layout = QVBoxLayout()

        # Görev çubuğu
        self.taskbar = QGridLayout()
        self.taskbar.setAlignment(Qt.AlignLeft)  # Solda hizala

        # Uygulama butonları
        open_file_manager_button = QPushButton("📁 Dosya Yöneticisi", self)
        open_file_manager_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: rgba(255, 255, 255, 0.7); border: 1px solid #ccc;")
        open_file_manager_button.clicked.connect(self.open_file_manager)
        self.taskbar.addWidget(open_file_manager_button, 0, 0)

        open_settings_button = QPushButton("⚙️ Ayarlar", self)
        open_settings_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: rgba(255, 255, 255, 0.7); border: 1px solid #ccc;")
        open_settings_button.clicked.connect(self.open_settings)
        self.taskbar.addWidget(open_settings_button, 0, 1)

        open_browser_button = QPushButton("🌐 Tarayıcı", self)
        open_browser_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: rgba(255, 255, 255, 0.7); border: 1px solid #ccc;")
        open_browser_button.clicked.connect(self.open_browser)
        self.taskbar.addWidget(open_browser_button, 0, 2)

        open_notepad_button = QPushButton("📝 Not Defteri", self)
        open_notepad_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: rgba(255, 255, 255, 0.7); border: 1px solid #ccc;")
        open_notepad_button.clicked.connect(self.open_custom_notepad)
        self.taskbar.addWidget(open_notepad_button, 0, 3)

        open_calculator_button = QPushButton("🧮 Hesap Makinesi", self)
        open_calculator_button.setStyleSheet("font-size: 16px; padding: 10px; background-color: rgba(255, 255, 255, 0.7); border: 1px solid #ccc;")
        open_calculator_button.clicked.connect(self.open_custom_calculator)
        self.taskbar.addWidget(open_calculator_button, 0, 4)

        layout.addLayout(self.taskbar)

        # Arka plan resmi
        self.background_label = QLabel(self)
        self.background_label.setPixmap(QPixmap("background.jpg"))  # Varsayılan arka plan resmi
        self.background_label.setScaledContents(True)  # Resmi ölçeklendir
        layout.addWidget(self.background_label)

        # Analog saat widget'ı
        self.clock_widget = AnalogClock(self)
        self.clock_widget.setFixedSize(200, 200)  # Saat boyutunu ayarlayın
        layout.addWidget(self.clock_widget, alignment=Qt.AlignTop | Qt.AlignCenter)  # Üstte ve ortada konumlandırın

        # Görev çubuğunun altında bir çizgi
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Ana içerik alanı
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file_manager(self):
        file_manager = FileManager(self)
        file_manager.exec_()  # QDialog kullanarak aç

    def open_settings(self):
        settings_window = Settings(self)
        settings_window.exec_()  # Ayarlar penceresini aç

    def open_system_info(self):
        system_info_window = SystemInfo(self)
        system_info_window.exec_()  # Sistem bilgileri penceresini aç

    def open_browser(self):
        browser_window = Browser(self)
        browser_window.exec_()  # Tarayıcı penceresini aç

    def open_custom_notepad(self):
        notepad_window = CustomNotepad(self)
        notepad_window.exec_()  # Kendi not defteri penceresini aç

    def open_custom_calculator(self):
        calculator_window = CustomCalculator(self)
        calculator_window.exec_()  # Kendi hesap makinesi penceresini aç

    def open_web_app(self, url):
        browser_window = Browser(self)
        browser_window.browser.setUrl(QUrl(url))  # Web uygulamasını aç
        browser_window.exec_()  # Tarayıcı penceresini aç

    def open_minesweeper(self):
        minesweeper_window = Minesweeper(self)
        minesweeper_window.exec_()  # Mayın tarlası penceresini aç

    def open_guide(self):
        guide_window = Guide(self)
        guide_window.exec_()  # Kullanım kılavuzu penceresini aç

class FileManager(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dosya Yöneticisi")
        self.setGeometry(150, 150, 600, 400)
        self.setStyleSheet("background-color: #FFFFFF;")  # Arka plan rengi

        self.layout = QVBoxLayout()
        self.file_list = QListWidget()
        self.layout.addWidget(self.file_list)

        self.load_files_button = QPushButton("📂 Dosyaları Yükle", self)
        self.load_files_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.load_files_button.clicked.connect(self.load_files)
        self.layout.addWidget(self.load_files_button)

        self.delete_file_button = QPushButton("🗑️ Dosyayı Sil", self)
        self.delete_file_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.delete_file_button.clicked.connect(self.delete_file)
        self.layout.addWidget(self.delete_file_button)

        self.open_file_button = QPushButton("📂 Dosyayı Aç", self)
        self.open_file_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.open_file_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_file_button)

        self.create_folder_button = QPushButton("📁 Yeni Klasör Oluştur", self)
        self.create_folder_button.setStyleSheet("font-size: 16px; padding: 10px;")
        self.create_folder_button.clicked.connect(self.create_folder)
        self.layout.addWidget(self.create_folder_button)

        self.setLayout(self.layout)

    def load_files(self):
        directory = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if directory:
            self.file_list.clear()
            for filename in os.listdir(directory):
                self.file_list.addItem(filename)

    def delete_file(self):
        selected_item = self.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            reply = QMessageBox.question(self, 'Dosyayı Sil', f'{file_name} dosyasını silmek istediğinize emin misiniz?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                os.remove(file_name)
                self.load_files()  # Dosyayı sildikten sonra dosya listesini güncelle

    def open_file(self):
        selected_item = self.file_list.currentItem()
        if selected_item:
            file_name = selected_item.text()
            if os.path.isfile(file_name):
                subprocess.Popen(["start", file_name], shell=True)  # Varsayılan uygulamada dosyayı aç

    def create_folder(self):
        folder_name, ok = QInputDialog.getText(self, 'Yeni Klasör', 'Klasör adı:')
        if ok and folder_name:
            os.makedirs(folder_name, exist_ok=True)  # Klasörü oluştur

class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ayarlar")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: #FFFFFF;")  # Arka plan rengi

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ayarlarınızı buradan yapabilirsiniz.", self))

        # Tema değiştirme
        theme_label = QLabel("Tema Seçin:", self)
        layout.addWidget(theme_label)

        self.theme_combo = QComboBox(self)
        self.theme_combo.addItems(["Açık Tema", "Koyu Tema"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)  # Tema değiştiğinde işlevi çağır
        layout.addWidget(self.theme_combo)

        # Uygulama dili değiştirme
        language_label = QLabel("Dil Seçin:", self)
        layout.addWidget(language_label)

        self.language_combo = QComboBox(self)
        self.language_combo.addItems(["Türkçe", "İngilizce"])
        self.language_combo.currentIndexChanged.connect(self.change_language)  # Dil değiştiğinde işlevi çağır
        layout.addWidget(self.language_combo)

        # Arka plan resmi yükleme butonu
        load_background_button = QPushButton("🖼️ Arka Plan Resmi Yükle", self)
        load_background_button.clicked.connect(self.load_background)
        layout.addWidget(load_background_button)

        # Arka plan rengi değiştirme butonu
        change_color_button = QPushButton("🎨 Arka Plan Rengini Değiştir", self)
        change_color_button.clicked.connect(self.change_background_color)
        layout.addWidget(change_color_button)

        self.setLayout(layout)

    def load_background(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if file_name:
            # Ana pencerenin arka planını değiştir
            self.parent().background_label.setPixmap(QPixmap(file_name))

    def change_background_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.parent().setStyleSheet(f"background-color: {color.name()};")  # Ana pencerenin arka plan rengini değiştir

    def change_theme(self):
        theme = self.theme_combo.currentText()
        if theme == "Açık Tema":
            self.parent().setStyleSheet("background-color: #F0F0F0;")  # Açık tema
        else:
            self.parent().setStyleSheet("background-color: #333333; color: #8B4513;")  # Koyu tema, yazı rengi kerem rengi

    def change_language(self):
        language = self.language_combo.currentText()
        QMessageBox.information(self, "Dil Değiştirildi", f"Uygulama dili {language} olarak değiştirildi.")

class Guide(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kullanım Kılavuzu")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: #FFFFFF;")  # Arka plan rengi

        layout = QVBoxLayout()

        # Kullanım kılavuzunu gösteren etiket
        guide_text = QLabel("Bu işletim sistemi ile ilgili temel bilgiler:\n\n"
                            "1. Dosya Yöneticisi: Dosyalarınızı yönetmek için kullanın.\n"
                            "2. Ayarlar: Tema ve dil ayarlarını değiştirebilirsiniz.\n"
                            "3. Tarayıcı: İnternette gezinmek için kullanın.\n"
                            "4. Not Defteri: Notlarınızı almak için kullanın.\n"
                            "5. Hesap Makinesi: Matematiksel işlemler yapmak için kullanın.\n"
                            "6. Mayın Tarlası: Eğlenceli bir oyun oynayın.\n"
                            "7. Sohbet Uygulaması: Diğer kullanıcılarla iletişim kurun.\n"
                            "8. Quiz Uygulaması: Bilgilerinizi test edin.", self)
        layout.addWidget(guide_text)

        self.setLayout(layout)

class SystemInfo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sistem Bilgileri")
        self.setGeometry(200, 200, 400, 300)
        self.setStyleSheet("background-color: #FFFFFF;")  # Arka plan rengi

        layout = QVBoxLayout()

        # Sistem bilgilerini gösteren etiketler
        system_info = f"Sistem: {platform.system()}\nSürüm: {platform.version()}\nİsim: {platform.node()}"
        info_label = QLabel(system_info, self)
        layout.addWidget(info_label)

        self.setLayout(layout)

class Browser(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Web Tarayıcısı")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Web tarayıcısı
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))  # Varsayılan URL
        layout.addWidget(self.browser)

        self.setLayout(layout)

class CustomNotepad(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kendi Not Defterimiz")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit(self)  # Basit bir metin girişi
        layout.addWidget(self.text_edit)

        save_button = QPushButton("Kaydet", self)
        save_button.clicked.connect(self.save_note)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_note(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Notu Kaydet", "", "Text Files (*.txt);;All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w') as file:
                file.write(self.text_edit.toPlainText())  # Metni dosyaya yaz

class CustomCalculator(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kendi Hesap Makinemiz")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()
        self.result_label = QLabel("Sonuç: ", self)
        layout.addWidget(self.result_label)

        # Giriş alanları
        self.input1 = QLineEdit(self)
        self.input2 = QLineEdit(self)
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)

        # İşlem butonları
        add_button = QPushButton("Topla", self)
        add_button.clicked.connect(self.calculate_sum)
        layout.addWidget(add_button)

        subtract_button = QPushButton("Çıkar", self)
        subtract_button.clicked.connect(self.calculate_subtract)
        layout.addWidget(subtract_button)

        multiply_button = QPushButton("Çarp", self)
        multiply_button.clicked.connect(self.calculate_multiply)
        layout.addWidget(multiply_button)

        divide_button = QPushButton("Böl", self)
        divide_button.clicked.connect(self.calculate_divide)
        layout.addWidget(divide_button)

        self.setLayout(layout)

    def calculate_sum(self):
        self.calculate_operation(lambda x, y: x + y)

    def calculate_subtract(self):
        self.calculate_operation(lambda x, y: x - y)

    def calculate_multiply(self):
        self.calculate_operation(lambda x, y: x * y)

    def calculate_divide(self):
        self.calculate_operation(lambda x, y: x / y if y != 0 else "Hata: Bölme sıfıra yapılamaz!")

    def calculate_operation(self, operation):
        try:
            num1 = float(self.input1.text())
            num2 = float(self.input2.text())
            result = operation(num1, num2)
            self.result_label.setText(f"Sonuç: {result}")
        except ValueError:
            self.result_label.setText("Geçersiz giriş!")

class Minesweeper(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mayın Tarlası")
        self.setGeometry(100, 100, 400, 400)

        self.grid_size = 10
        self.mines_count = 10
        self.buttons = []
        self.mines = []

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        self.create_grid()
        self.place_mines()

    def create_grid(self):
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                button = QPushButton("")
                button.setFixedSize(30, 30)
                button.clicked.connect(lambda checked, x=i, y=j: self.reveal_cell(x, y))
                self.layout.addWidget(button, i, j)
                row.append(button)
            self.buttons.append(row)

    def place_mines(self):
        while len(self.mines) < self.mines_count:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if (x, y) not in self.mines:
                self.mines.append((x, y))

    def reveal_cell(self, x, y):
        if (x, y) in self.mines:
            self.buttons[x][y].setText("💣")
            QMessageBox.critical(self, "Kaybettiniz!", "Mayına bastınız!")
            self.close()
        else:
            self.buttons[x][y].setText("0")  # Burada gerçek sayı hesaplaması yapılabilir

def main():
    app = QApplication([])
    os = SimpleOS()
    os.show()
    app.exec_()

if __name__ == "__main__":
    main()