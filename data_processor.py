from SignalParser.Patch2Parser import Patch2Parser
from SignalParser.PatchMParser import PatchMParser
class DataProcessor:
    def __init__(self):
        """BLE 데이터 처리 클래스 - 신호 키에 따라 적절한 파서 매핑"""
        self.parsers = {
            "pach2": Patch2Parser(lambda x: (x << 4) * 191*(10**-6)),
            "patchM" : PatchMParser(lambda x: x * 0.0028228759765625),
        }

    def process(self, raw_data: bytes, key_prefix: str = "signal") -> dict:
        """
        신호 키에 따라 적절한 파서 클래스를 호출하여 데이터를 처리함

        Args:
            raw_data (bytes): BLE 수신 데이터
            key_prefix (str): 처리 대상 신호 접두사 (예: 'signal_1')

        Returns:
            dict: 파싱된 데이터 (key: 신호 인덱스, value: 변환 결과)
        """
        parser = self.parsers.get(key_prefix)
        if parser:
            try:
                return parser.parse(raw_data, key_prefix)
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"error": f"Unsupported signal key prefix: {key_prefix}"}