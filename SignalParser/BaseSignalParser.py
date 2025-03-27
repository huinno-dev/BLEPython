class BaseSignalParser:
    def __init__(self, formula=lambda x: x):
        # 각 샘플에 적용할 수식(변환 함수)을 저장
        self.formula = formula

    def parse(self, raw_data: bytes, key_prefix: str) -> dict:
        # 하위 클래스에서 반드시 구현해야 하는 추상 메서드
        raise NotImplementedError("parse method must be implemented in subclass")