from aiortc import VideoStreamTrack, RTCPeerConnection, RTCSessionDescription
from aiortc.contrib.signaling import TcpSocketSignaling
import cv2
import asyncio

class WebcamVideoStreamTrack(VideoStreamTrack):
    def __init__(self, camera_id: int) -> None:
        super().__init__()
        self.web_cam = cv2.VideoCapture(camera_id)
        
        # juste un print, mais en principe ya rien qui va se passer si la caméra ouvre pas...
        if not self.web_cam.isOpened():
            print(f"Could not open camera with id {camera_id}")

    async def recv(self) -> cv2.typing.MatLike | None:
        valid, video_frame = self.web_cam.read()
        
        if not valid: 
            return None
        
        # faire les ajustements videos ici
        # modifications couleurs, stretch, etc.
        
        return video_frame



async def setup_and_run_server(server_ip: str, server_port: int, webcam_id: int) -> None:
    signaling = TcpSocketSignaling(server_ip, server_port)
    connection = RTCPeerConnection()
    video_streamer = WebcamVideoStreamTrack(webcam_id)

    # Négociation des paramètres
    async with connection:
        await signaling.connect()

        offer = await connection.createOffer()
        await connection.setLocalDescription(offer)
        await signaling.send(connection.localDescription)

        while True:
            obj = await signaling.receive()
            if isinstance(obj, RTCSessionDescription):
                await connection.setRemoteDescription(obj)
                print("Remote description set")
            elif obj is None:
                print("Signaling ended")
                break
        print("Closing connection")

        
async def main():
    # ip de ta mère
    ip_address = "127.0.0.1"
    # port ouvert pour tests, n'importe quel port ouvert marche
    port = 9999
    # typiquement 0 pour la webcam principale du laptop
    camera_id = 0
    await setup_and_run_server(ip_address, port, camera_id)


asyncio.run(main())