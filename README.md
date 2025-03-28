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
├── SignalParser              # 신호 Parser 
    ├── BaseSignalParser.py
    ├── Patch2Parser.py
    ├── PatchMParser.py
├── device_profiles           # 디바이스 정의 - indi, noti
    ├── __init__.py
    ├── base_profile.py
    ├── device_patch2.py
    ├── device_patchM.py
├── main.py                   # PyQt GUI 실행 및 BLEManager 연동
├── ble_manager.py            # BLE 연결, 명령 송신, 알림 수신 핸들링
├── data_processor.py         # 수신 데이터 가공 (FFT, 필터 등 적용 가능)
├── data_visualizer_dialog.py # PyQt 실시간 시각화 다이얼로그
