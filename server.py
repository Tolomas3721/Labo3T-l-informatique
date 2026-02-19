from aiortc import VideoStreamTrack, RTCPeerConnection, TcpSocketSignaling
import cv2
import asyncio

class WebcamVideoStreamTrack(VideoStreamTrack):
    #Surcharge du constructeur
    def __init__(self, camera_id):
        super().__init__()
        self.web_cam = cv2.VideoCapture(camera_id)
        if not self.web_cam.isOpened():
            print(f"Could not open camera with id {camera_id}")

    async def recv(self):
        #Ajouter ici la logique pour récupérer et traiter une trame vidéo puis retournez la trame vidéo capturée.
        valid, video_frame = self.web_cam.read()
        
        if not valid: 
            return None
        
        return video_frame



async def setup_and_run_server(server_ip, server_port, webcam_id):
    signaling = ...
    connection = ...
    video_streamer = ...

    ... #Négociation des paramètres

    while True:
        ...
        
async def main():
    ip_address = ...
    port = ...
    camera_id = ...
    await setup_and_run_server(ip_address, port, camera_id)


asyncio.run(main())