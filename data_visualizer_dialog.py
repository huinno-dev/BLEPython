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

    def append_data(self, parsed):
        needs_update = False
        for key in sorted(parsed.keys()):
            value = parsed[key]["value"]
            self.data_buffer.append(QPointF(self.sample_index/self.sps, value))
            self.sample_index += 1
            needs_update = True

            if self.sample_index >= self.max_samples:
                self.series.clear()
                self.data_buffer.clear()
                self.sample_index = 0

        if needs_update:
            self.update_chart()

    def update_chart(self):
        for point in self.data_buffer:
            self.series.append(point)
        self.data_buffer.clear()