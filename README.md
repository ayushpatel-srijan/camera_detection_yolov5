Steps to Connect with PEM Key and Run MMM_PoC

1. Connect to the Server Using PEM Key
   - Open a terminal or command prompt.
   - Use the following command to connect to the server:
     ```
     ssh -i /path/to/pem/key.pem username@server_ip_address
     ```
     Replace `/path/to/pem/key.pem` with the actual path to your PEM key file, and `username@server_ip_address` with the appropriate username and IP address of the server you want to connect to.

2. Navigate to the MMM_PoC Folder
   - Use the following command to change to the MMM_PoC folder:
     ```
     cd MMM_PoC
     ```

3. Run Docker Compose
   - Once you are inside the MMM_PoC folder, use the following command to start the Docker Compose process:
     ```
     sudo docker-compose up
     ```
     This command will download any necessary dependencies and start the MMM_PoC application.

4. Monitor the Application
   - After running the above command, monitor the terminal or command prompt for any logs or output related to the MMM_PoC application.

5. Access the MMM_PoC Application
   - Once the Docker Compose process is running without any issues, you can access the MMM_PoC application by opening a web browser and entering the appropriate URL or IP address.

6. Interact with the MMM_PoC Application
   - Use the features and functionalities provided by the MMM_PoC application as needed.

7. Stop the MMM_PoC Application
   - To stop the MMM_PoC application and terminate the Docker Compose process, press `Ctrl + C` in the terminal or command prompt where it is running.

8. Disconnect from the Server
   - Once you are finished with the MMM_PoC application, use the following command to disconnect from the server:
     ```
     exit
     ```
