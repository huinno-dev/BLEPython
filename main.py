import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QListWidget, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from qasync import QEventLoop, asyncSlot
from bleak import BleakScanner
from ble_manager import BLEManager
from data_visualizer_dialog import DataVisualizerDialog

class BLEScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.ble_manager = None
        self.visualizer_dialog = None

    def initUI(self):
        self.setWindowTitle("BLE Scanner & Connector")
        self.setGeometry(100, 100, 500, 500)

        self.scan_button = QPushButton("🔍 스캔 시작", self)
        self.scan_button.clicked.connect(self.start_scan)

        self.connect_button = QPushButton("🔗 연결", self)
        self.connect_button.setEnabled(False)
        self.connect_button.clicked.connect(self.connect_device)

        self.disconnect_button = QPushButton("🔌 연결 해제", self)
        self.disconnect_button.setEnabled(False)
        self.disconnect_button.clicked.connect(self.disconnect_device)

        self.command_input = QLineEdit(self)
        self.command_input.setPlaceholderText("전송할 명령어 입력 (HEX)")

        self.send_command_button = QPushButton("📡 명령어 전송", self)
        self.send_command_button.setEnabled(False)
        self.send_command_button.clicked.connect(self.send_command)

        self.graph_button = QPushButton("📈 그래프 보기", self)
        self.graph_button.setEnabled(False)
        self.graph_button.clicked.connect(self.show_graph)

        self.device_list = QListWidget(self)
        self.device_list.itemSelectionChanged.connect(self.enable_connect_button)

        self.status_label = QLabel("상태: ❌ 연결되지 않음", self)

        layout = QVBoxLayout()
        layout.addWidget(self.scan_button)
        layout.addWidget(self.device_list)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.command_input)
        layout.addWidget(self.send_command_button)
        layout.addWidget(self.graph_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    @asyncSlot()
    async def start_scan(self):
        self.device_list.clear()
        self.scan_button.setEnabled(False)
        devices = await BleakScanner.discover()
        self.scan_button.setEnabled(True)

        filtered_devices = [
            (device.name or "Unknown", device.address)
            for device in devices 
            if isinstance(device.name, str) and "MPT_P" in device.name
        ]

        for name, address in filtered_devices:
            self.device_list.addItem(f"{name} - {address}")

    def enable_connect_button(self):
        self.connect_button.setEnabled(bool(self.device_list.selectedItems()))

    @asyncSlot()
    async def connect_device(self):
        selected_item = self.device_list.currentItem()
        if selected_item:
            device_address = selected_item.text().split(" - ")[-1]
            device_name = selected_item.text().split(" - ")[0]
            self.ble_manager = BLEManager(device_address, device_name, log_func=self.log)
            self.visualizer_dialog = DataVisualizerDialog(self)
            self.ble_manager.attach_visualizer(self.visualizer_dialog)

            success = await self.ble_manager.connect()
            if success:
                self.status_label.setText(f"상태: ✅ 연결됨: {device_address}")
                self.disconnect_button.setEnabled(True)
                self.send_command_button.setEnabled(True)
                self.graph_button.setEnabled(True)
            else:
                self.status_label.setText("상태: ❌ 연결 실패")

    @asyncSlot()
    async def disconnect_device(self):
        if self.ble_manager:
            await self.ble_manager.disconnect()
            self.status_label.setText("상태: 🔌 연결 해제됨")
            self.disconnect_button.setEnabled(False)
            self.send_command_button.setEnabled(False)
            self.graph_button.setEnabled(False)

    @asyncSlot()
    async def send_command(self):
        command_hex = self.command_input.text().strip()
        if command_hex and self.ble_manager:
            try:
                command_bytes = bytes.fromhex(command_hex)
                await self.ble_manager.send_command(command_bytes)
            except ValueError:
                self.status_label.setText("⚠️ 잘못된 HEX 입력")

    def show_graph(self):
        if self.visualizer_dialog:
            self.visualizer_dialog.show()

    def log(self, message):
        print(message)  # 추후 UI 로그 출력으로 확장 가능

if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = BLEScannerApp()
    window.show()

    with loop:
        loop.run_forever()