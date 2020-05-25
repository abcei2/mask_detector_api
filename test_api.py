'''
This code is an example in the way we could use this api
command:
* register: to register a new face.
* proccess: to detect and classify faces on an image.
name:
* name of register face, only work when command='register'.
**************
update_model: local variable True if you want to update the model, 
False if you want to register or detect faces
'''

import requests
import os
import json
import cv2


web_camera=True
ip_of_api="192.168.1.2"
port_of_api="5000"
path_image="/home/santi/Downloads/90442488_4188275714531241_492913197330726912_n.jpg"

if not web_camera:

    frame=cv2.imread(path_image)
    frame=cv2.imencode(".jpg", frame)[1]

    ### UPLOAD IMAGE 
    files = {'file': ('image.jpg', frame, 'multipart/form-data')}

    response = requests.post(f'http://{ip_of_api}:{port_of_api}/detect_faces',
                                files=files)
else:
    cap=cv2.VideoCapture(0)
    while True:
        ret, frame= cap.read()
        fram_draw=frame.copy()
        frame_to_upload=cv2.imencode(".jpg", frame)[1]
        ### UPLOAD IMAGE 
        files = {'file': ('image.jpg', frame_to_upload, 'multipart/form-data')}

        response = requests.post(f'https://ai.tucanoar.com/faces/detect_faces/',
                                    files=files)
        #print(response.json())
        detections=response.json()
        for faces in detections['message']['faces_detected']:
            print(faces)

            face_image=frame[faces['upper_left'][1]:faces['down_right'][1], faces['upper_left'][0]:faces['down_right'][0]]
     
                
            face_image_to_upload=cv2.imencode(".jpg", face_image)[1]
            ### UPLOAD IMAGE 
            files = {'file': ('image.jpg', face_image_to_upload, 'multipart/form-data')}

            response = requests.post(f'http://localhost:5000/detect_mask/',
                                        files=files)
            print(response.json())
            
            if response.json()["message"]["with_mask"]:
                color_mask=(0,200,0)
            else:
                color_mask=(0,0,200)

            cv2.rectangle(
                fram_draw,
                (faces['upper_left'][0],faces['upper_left'][1]),
                (faces['down_right'][0],faces['down_right'][1]),
                color_mask
            )
            for landmark in faces["landmarks"]:
                print(landmark)
                cv2.circle(fram_draw, (landmark[0],landmark[1]),  2, color_mask, -1) 
      
            
        cv2.imshow("frame with faces",fram_draw)
        cv2.waitKey(50)