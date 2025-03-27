from .BaseSignalParser import BaseSignalParser
class PatchMParser(BaseSignalParser):
    def __init__(self, formula=None):
        super().__init__(formula)
        
    def parse(self, raw_data: bytes, key_prefix: str) -> dict:
        """240바이트 raw_data를 12비트 단위로 파싱하는 파서"""
        parsed = {}
        if len(raw_data) != 244:
            return {"error": f"Expected 244 bytes, got {len(raw_data)}"}

        prefix = int.from_bytes(raw_data[0:4],"little")
        ecg_data = raw_data[4:184]

        for i in range(0, len(ecg_data), 3):
            if i + 2 >= len(ecg_data):
                break

            b0 = ecg_data[i]
            b1 = ecg_data[i + 1]
            b2 = ecg_data[i + 2]

            # 첫 번째 샘플 (12비트)
            raw1 = (b0 << 4) | ((b1 & 0xF0) >> 4)
            if raw1 & 0x800:
                raw1 -= 0x1000
            key1 = f"{key_prefix}_{(i // 3) * 2 + 1 + prefix}"
            parsed[key1] = {"raw": raw1, "value": self.formula(raw1)}

            # 두 번째 샘플 (12비트)
            raw2 = ((b1 & 0x0F) <<8) | b2
            if raw2 & 0x800:
                raw2 -= 0x1000
            key2 = f"{key_prefix}_{(i // 3) * 2 + 2 + prefix}"
            parsed[key2] = {"raw": raw2, "value": self.formula(raw2)}

        return parsed