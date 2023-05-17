Steps to Connect with PEM Key and Run Docker Compose

1. Connect using PEM Key:
   - Open your terminal or command prompt.
   - Use the following command to connect to the server with the PEM key:
     ```
     ssh -i camera_detection_keypair.pem user@your_server_ip
     ```
     Replace `camera_detection_keypair.pem` with the path to your PEM key file, and `user@your_server_ip` with the appropriate user and server IP.

2. Navigate to the "camera_detection_yolov5" Folder:
   - Once connected to the server, use the `cd` command to navigate to the "camera_detection_yolov5" folder.
     ```
     cd camera_detection_yolov5
     ```

3. Run Docker Compose:
   - After navigating to the "camera_detection_yolov5" folder, use the following command to run Docker Compose:
     ```
     sudo docker-compose up
     ```
   - This command will start the Docker Compose process and provide the specific link

