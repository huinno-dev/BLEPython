from PyQt5.QtWidgets import QDialog, QVBoxLayout
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QTimer, QPointF

class DataVisualizerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📈 실시간 데이터 시각화")
        self.resize(600, 400)

        self.series = QLineSeries()
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.createDefaultAxes()
        self.chart.setTitle("BLE 데이터 스트림")
        
        self.chart.axisX().setRange(0,10)
        self.chart.axisY().setRange(-5, 5)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.chart_view)
        self.setLayout(self.layout)

        self.sample_index = 0
        self.sps = 250  # Samples per second
        self.max_seconds = 10
        self.max_samples = self.sps * self.max_seconds

        self.data_buffer = []
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_chart)
        self.timer.setInterval(int(1000 / self.sps))
        self.is_receiving = False
        self.batch_size = max(1, self.sps // 20)  # 50Hz로 약 5포인트씩 보여주기
        
    def append_data(self, parsed):
        if not self.is_receiving:
            self.timer.start()
            self.is_receiving = True
            
        for key in sorted(parsed.keys()):
            value = parsed[key]["value"]
            self.data_buffer.append(QPointF(self.sample_index/self.sps, value))
            self.sample_index += 1

            if self.sample_index >= self.max_samples:
                self.series.clear()
                self.data_buffer.clear()
                self.sample_index = 0

    def update_chart(self):
        if not self.data_buffer:
            self.timer.stop()
            self.is_receiving = False
            return

        for _ in range(min(len(self.data_buffer), self.batch_size)):
            point = self.data_buffer.pop(0)
            self.series.append(point)