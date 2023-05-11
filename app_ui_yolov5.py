import cv2
import streamlit as st
import time
import pyscreenshot as ImageGrab
import os
import torch


class YOLOVDetection:
    
    def __init__(self, weights="yolov5m_Objects365.pt"):
        self.weights = weights
        self.model = None
        self.device = None
        self.load_model()
        
    def load_model(self):
        self.model = torch.hub.load('yolov5', 'custom', path=self.weights, source='local') 
        self.model.classes = 61,63
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.model.to(self.device)
        
    def predict(self, frame):
        # Run detection
        results = self.model(frame)
        df = results.pandas().xyxy[0]
        my_dict = {}
        for k, v in zip(df['name'], df['confidence']):
            if k not in my_dict or v > my_dict[k]:
                my_dict[k] = v
        return my_dict



class CameraDetection:
    
    def __init__(self):
        self.yolov = YOLOVDetection()
        self.video_feed = None
        self.container = None
        self.cap = cv2.VideoCapture(0)
        self.frame_count = 0
        
        # Convert the color format once
        self.color_conversion = cv2.COLOR_BGR2RGB
        
        # Define the objects to detect and their thresholds
        self.objects_to_detect = ["Cell Phone", "Camera"]
        self.threshold = 0.3
        
    def run(self):
        st.title("Camera Detection Demo - YOLOV5 Custom")
        self.video_feed = st.empty()
        self.container = st.empty()
        
        # Check the results and generate message outside the loop
        def check_results(result_dict):
            message = None
            for obj in self.objects_to_detect:

                if obj in result_dict.keys() and result_dict[obj] > self.threshold:
                    message = f"{obj} Detected - {result_dict[obj]:.1%}"
                    break
                else:
                    print(result_dict.keys() )
            return message
        
        # Convert the frame to the correct color format once
        def convert_frame(frame):
            return cv2.cvtColor(frame, self.color_conversion)
        
        # Process the video feed
        while True:
            ret, frame = self.cap.read()
            self.frame_count += 1
            if ret:
                # Convert the frame to the correct color format
                frame = convert_frame(frame)
                self.video_feed.image(frame, channels="RGB")
                frame = cv2.resize(frame,(640,640))
                result_dict = self.yolov.predict(frame)
                message = check_results(result_dict)
                if message:
                    self.container.error(message, icon="🚨")
                    if not os.path.exists("output_frames"):
                        os.mkdir("output_frames")
                    filename = os.path.join("output_frames", f"frame_{self.frame_count}.jpg")
                    cv2.imwrite(filename, frame)
                    screenshot = ImageGrab.grab()
                    screenshot.save(f"output_frames/screenshot_{self.frame_count}.png")
                    self.container.empty()

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()



if __name__ == '__main__':
    detector = CameraDetection()
    detector.run()
