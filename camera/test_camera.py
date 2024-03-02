import sys
import cv2
import threading
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox


class VideoRecorder:
    def __init__(self):
        self.capture_duration = 60  # 录制持续时间（单位：秒）
        self.is_recording = False

    def start_recording(self):
        self.is_recording = True
        threading.Thread(target=self._record_video).start()

    def _record_video(self):
        # 打开摄像头
        cap = cv2.VideoCapture(0)  # 参数0表示打开第一个摄像头，如果有多个摄像头，可以尝试不同的索引值

        # 检查摄像头是否成功打开
        if not cap.isOpened():
            print("无法打开摄像头")
            return

        # 获取摄像头的帧率
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # 获取摄像头的分辨率
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 定义视频编码器和输出文件名
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_filename = 'output_video.mp4'

        # 创建视频写入对象
        out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

        # 记录开始录制的时间
        start_time = cv2.getTickCount()

        while self.is_recording:
            # 读取一帧视频
            ret, frame = cap.read()

            # 检查视频是否成功读取
            if not ret:
                print("无法获取视频帧")
                break

            # 将帧写入输出视频文件
            out.write(frame)

            # 检查是否达到了录制持续时间
            current_time = cv2.getTickCount()
            if (current_time - start_time) / cv2.getTickFrequency() >= self.capture_duration:
                break

        # 释放摄像头资源和输出视频文件
        cap.release()
        out.release()

        print("视频已保存为:", output_filename)

    def stop_recording(self):
        self.is_recording = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("视频录制器")
        self.setGeometry(100, 100, 300, 200)

        self.video_recorder = VideoRecorder()
        # 按钮一
        self.start_button = QPushButton("开始录制", self)
        self.start_button.setGeometry(50, 50, 200, 50)
        self.start_button.clicked.connect(self.start_recording)
        # 按钮二
        self.test_button = QPushButton("测试摄像头", self)
        self.test_button.setGeometry(50, 10, 200, 50)
        self.test_button.clicked.connect(self.video_show)
        # 按钮三
        self.stop_button = QPushButton("stop_video", self)
        self.stop_button.setGeometry(50, 100, 200, 50)
        self.stop_button.clicked.connect(self.stop_video)

    def start_recording(self):
        self.start_button.setEnabled(False)
        self.video_recorder.start_recording()
        QMessageBox.information(self, "提示", "开始录制视频，请等待1分钟。")

    @staticmethod
    def video_show(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("can't open the camera! ")
            exit()
        while True:
            ret, frame = cap.read()
            if not ret:
                print("can't get the video from the camera! ")
                exit()
            cv2.imshow("camera", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        # cv2.destroyWindow()
        cv2.destroyAllWindows()

    def stop_video(self):
        self.video_recorder.stop_recording()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
