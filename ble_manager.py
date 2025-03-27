
import asyncio
from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from data_processor import DataProcessor  # 데이터 가공 모듈
from data_visualizer_dialog import DataVisualizerDialog  # PyQt 기반 실시간 시각화 다이얼로그

# Command & Notification Characteristic UUIDs
COMMAND_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"  # 명령어 전송용 (Write)
NOTIFICATION_UUID = "0000fff5-0000-1000-8000-00805f9b34fb"  # 알림 수신용 (Notify)
CCCD_UUID = "00002902-0000-1000-8000-00805f9b34fb"  # Client Characteristic Configuration Descriptor

class BLEManager:
    def __init__(self, device_address, device_name, log_func=print):
        """BLEManager 클래스 초기화: 장치 주소와 로그 출력 함수를 설정"""
        self.device_address = device_address
        self.client = BleakClient(self.device_address)
        self.is_connected = False
        self.log = log_func
        self.processor = DataProcessor()
        self.visualizer = None  # 나중에 연결될 수 있도록 지연 초기화
        self.device_name = device_name

    def attach_visualizer(self, visualizer_dialog):
        """PyQt 기반 시각화 다이얼로그를 BLEManager에 연결"""
        self.visualizer = visualizer_dialog

    async def handle_indication(self, sender, data):
        """FFF2 Indication 수신 시 호출되는 콜백"""
        self.log(f"📩 [FFF2 Indication] {data.hex()}")
#        parsed = self.processor.process(data, 'patchM')
#        if self.visualizer:
#            self.visualizer.append_data(parsed)

    async def handle_notification(self, sender, data):
        """FFF5 Notification 수신 시 호출되는 콜백"""
#        self.log(f"📩 [FFF5 Notification] {data.hex()}")
        parsed = self.processor.process(data, 'patchM')
        if self.visualizer:
            self.visualizer.append_data(parsed)

    async def connect(self):
        """BLE 장치에 연결하고 GATT 서비스 및 알림/인디케이션 설정"""
        try:
            await self.client.connect()
            if self.client.is_connected:
                self.is_connected = True
                self.log(f"✅ 연결됨: {self.device_address}")

                services = await self.client.get_services()

                self.log("\n🔍 Discovered Services & Characteristics:")
                for service in services:
                    self.log(f"  - Service: {service.uuid}")
                    for char in service.characteristics:
                        self.log(f"    └ Characteristic: {char.uuid} (Properties: {char.properties})")

                await self.register_UUID()
                return True
            else:
                self.log("❌ 연결 실패")
                return False
        except Exception as e:
            self.log(f"⚠️ 연결 오류: {e}")
            return False

    async def register_UUID(self):
        """UUID에 대한 알림/인디케이션 활성화"""
        await self.client.start_notify(COMMAND_UUID, self.handle_indication)
        self.log(f"📩 Indication 활성화됨: {COMMAND_UUID}")
        
        await self.client.start_notify(NOTIFICATION_UUID, self.handle_notification)
        self.log(f"📩 Notification 활성화됨: {NOTIFICATION_UUID}")

    async def disconnect(self):
        """BLE 장치 연결 해제"""
        if self.client and self.is_connected:
            await self.client.disconnect()
            self.is_connected = False
            self.log("🔌 연결 해제됨")

    async def send_command(self, command: bytes, timeout: float = 5.0):
        """FFF2 UUID에 명령어 전송 (최대 20바이트, 부족하면 패딩)"""
        if self.is_connected:
            try:
                if len(command) < 20:
                    command = command.ljust(20, b'\x00')
                await self.client.write_gatt_char(COMMAND_UUID, command, response=True)
                self.log(f"📡 Command sent: {command.hex()}")
            except Exception as e:
                self.log(f"⚠️ Command send failed: {e}")