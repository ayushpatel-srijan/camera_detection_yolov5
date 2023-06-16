import cv2
import streamlit as st
import time
import pyscreenshot 
import os
import torch
import shutil

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
    
    def __init__(self,mode="webcam",path=None):
        self.yolov = YOLOVDetection()
        self.video_feed = None
        self.container = None
        if mode=="webcam":
            self.cap = cv2.VideoCapture(0)
        elif mode=="video":
            self.cap = cv2.VideoCapture(path)
         
        self.frame_count = 0
        
        # Convert the color format once
        self.color_conversion = cv2.COLOR_BGR2RGB
        
        # Define the objects to detect and their thresholds
        self.objects_to_detect = ["Cell Phone", "Camera"]
        self.threshold = 0.2
        

    def run(self):
        self.video_feed = st.empty()
        self.container = st.empty()
        self.log_textbox = st.empty()
        self.log = []


        # Check the results and generate message outside the loop
        def check_results(result_dict, frame_time):
            message = None
            for obj in self.objects_to_detect:
                if obj in result_dict.keys() and result_dict[obj] > self.threshold:
                    message = f"{obj} Detected - {result_dict[obj]:.1%}"
                    self.log.append((frame_time, self.frame_count, obj,result_dict[obj]))
                    break
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
                frame = cv2.resize(frame, (640, 640))
                frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                result_dict = self.yolov.predict(frame)
                current_time = time.strftime("%H:%M:%S", time.localtime())
                message = check_results(result_dict, current_time)
                if message:
                    self.container.error(message, icon="🚨")
                    if not os.path.exists("output_frames"):
                        os.mkdir("output_frames")
                    filename = os.path.join("output_frames", f"frame_{self.frame_count}_{current_time}.jpg")
                    cv2.imwrite(filename, frame)
                    screenshot = pyscreenshot.grab()
                    screenshot.save(f"output_frames/screenshot_{self.frame_count}_{current_time}.png")
                    self.container.empty()
                log_text = ""
                for log_entry in self.log[::-1]:
                    log_text += f"Frame: {log_entry[1]}, Time: {log_entry[0]}, Object: {log_entry[2]}, Confidence: {log_entry[3]:.1%}\n"
                self.log_textbox.text(log_text)




if __name__ == '__main__':
    st.error("The information in this site is intended solely for the Demo purposes. While we have taken every precaution to ensure that the result is reasonably accurate, errors can occur. This should not be considered as a fully developed production level system with a high degree of accuracy, as training and tuning has been limited for the intended demo purpose.")
    st.markdown("---")
    st.title("Camera Detection Demo - YOLOV5 Custom")

    if os.path.exists("output_frames"):
        shutil.rmtree("output_frames")
        os.mkdir("output_frames")

    if st.checkbox("Webcam"):
        detector = CameraDetection()
        detector.run()

    if st.checkbox("Video"):
        accepted_formats = ['mp4']
        video_file = st.file_uploader('Upload a video file', type=accepted_formats)

        sample_videos = {
            "None":None,
            "Sample Video 1": "sample_video_1.mp4",
            "Sample Video 2": "sample_video_2.mp4"
        }
        selected_sample = st.selectbox("Select a sample video", list(sample_videos.keys()), index=0)

        if video_file:
            if not os.path.exists("videos"):
                os.mkdir("videos")
            with open(os.path.join('videos', video_file.name), 'wb') as f:
                f.write(video_file.read())
            st.success('Video saved successfully!')
            detector = CameraDetection(mode="video", path="videos/" + video_file.name)
            detector.run()

        elif selected_sample:
            sample_video_path = sample_videos[selected_sample]
            detector = CameraDetection(mode="video", path=sample_video_path)
            detector.run()

