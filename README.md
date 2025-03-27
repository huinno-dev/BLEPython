# 🔗 PyQt BLE GUI Sample

`PyQt BLE GUI Sample`은 Python `bleak`와 `PyQt` 기반으로 작성된 **BLE 장치 통신 및 실시간 데이터 시각화** 도구입니다.  
BLE 기기와 연결하여 명령어를 전송하고, Notification 및 Indication을 받아 **데이터를 처리 및 시각화**할 수 있습니다.

---

## 🚀 주요 기능

- ✅ **BLE 장치 연결 및 GATT 탐색**
- 📩 **Indicate Notify** 수신 처리
- 🧠 **데이터 가공 (DataProcessor 사용)**
- 📊 **PyQt 기반 실시간 데이터 시각화**
- 🧪 **BLE 명령어 전송 지원 (패딩 처리 포함)**

---

## 📦 프로젝트 구조

```text
.
├── main.py                   # PyQt GUI 실행 및 BLEManager 연동
├── ble_manager.py            # BLE 연결, 명령 송신, 알림 수신 핸들링
├── data_processor.py         # 수신 데이터 가공 (FFT, 필터 등 적용 가능)
├── SignalParser              # 신호 Parser 
    ├── BaseSignalParser.py
    ├── Patch2Parser.py
    ├── PatchMParser.py
├── data_visualizer_dialog.py # PyQt 실시간 시각화 다이얼로그

📡 동작 방식
BLE 장치 검색 및 연결 (BleakClient)

FFF2 UUID로 명령 전송 (Write)

FFF2 또는 FFF5 UUID로부터 Notification/Indication 수신

수신된 데이터를 파싱 및 시각화

🛠️ 사용 예시
python
복사
편집
manager = BLEManager("AA:BB:CC:DD:EE:FF")
await manager.connect()

# 명령 전송
await manager.send_command(b'\\x01\\x02')

# 종료 시
await manager.disconnect()
⚙️ 사용 라이브러리
bleak - Cross-platform BLE client

PyQt5 - GUI framework

asyncio - 비동기 이벤트 루프 처리

🧩 사전 조건
Python >= 3.9

BLE를 지원하는 OS 및 하드웨어

requirements.txt로 설치:

bash
복사
편집
pip install -r requirements.txt
📈 확장 아이디어
 다중 BLE 장치 연결

 실시간 로그 저장 (CSV)

 Web 기반 시각화 (FastAPI + WebSocket)

 장치 페어링 UI 추가

📝 라이선스
MIT License. 자유롭게 사용하세요!
