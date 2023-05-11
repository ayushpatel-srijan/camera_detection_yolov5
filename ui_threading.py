import torch
import cv2
import threading
import streamlit as st
import time
import os 
import pyscreenshot

class YOLOV5CustomModel:
    def __init__(self, weights_file_path, device):
        self.model = torch.hub.load('yolov5', 'custom', path=weights_file_path, source='local')
        self.model.classes = [61, 63]
        self.device = device
        self.model.to(self.device)
    
    def predict(self, frame):
        with torch.no_grad():
            results = self.model(frame)
            df = results.pandas().xyxy[0]
            return df['name'], df['confidence']

class CameraDetectionApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0
        self.result_dict = {}
        self.prediction_thread = None
        self.video_feed = st.empty()
        self.model = YOLOV5CustomModel("yolov5m_Objects365.pt", torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        
    def run(self):
        while True:
            message = None
            ret, frame = self.cap.read()
            self.frame_count += 1
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.video_feed.image(frame, channels="RGB")
                frame = cv2.resize(frame, (640, 640))

                if not self.prediction_thread or not self.prediction_thread.is_alive():
                    self.prediction_thread = threading.Thread(target=self.run_prediction, args=(frame,))
                    self.prediction_thread.start()
                
                print(self.result_dict)
                if "Cell Phone" in self.result_dict and self.result_dict["Cell Phone"] > 0.3:
                    message = f"Camera Device Detected - {self.result_dict['Cell Phone']:.1%}"
                elif "Camera" in self.result_dict and self.result_dict["Camera"] > 0.3:
                    message = f"Camera Device Detected - {self.result_dict['Camera']:.1%}"
                else:
                    message = None

                if message:
                    start =time.time()
                    container = st.empty()
                    container.error(message, icon="🚨") 
                    if not os.path.exists("output_frames"):
                        os.mkdir("output_frames")
                    filename = os.path.join("output_frames", f"frame_{self.frame_count}.jpg")
                    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                    cv2.imwrite(filename, frame)
                    print(f"file saved in {filename}")
                    screenshot = pyscreenshot.grab()
                    screenshot.save(f"output_frames/screenshot_{self.frame_count}.png")
                    print(f"Screenshot saved in output_frames/screenshot_{self.frame_count}.png")  # container.info, success we can use any
                    # time.sleep(2)  # Wait 2 seconds
                    container.empty()
                    end =time.time()
                    print("Predicted in : ",end - start)
                    self.result_dict ={}
    
    def run_prediction(self, frame):
        name, confidence = self.model.predict(frame)
        for k, v in zip(name, confidence):
            if k not in self.result_dict or v > self.result_dict[k]:
                self.result_dict[k] = v


if __name__ == '__main__':
    st.title("Camera Detection Demo - YOLOV5 Custom")
    app = CameraDetectionApp()
    app.run()


