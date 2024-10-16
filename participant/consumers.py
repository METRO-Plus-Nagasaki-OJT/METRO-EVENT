import json
import base64
from channels.generic.websocket import WebsocketConsumer

class ParticipantConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        image_base64 = text_data_json["image_url"]

        # Extract base64 data
        base64_data = image_base64.split(",")[1]

        # Decode base64 to bytes
        byte_data = base64.b64decode(base64_data)
        
        # Send back the received image
        self.send(text_data=json.dumps({"image_url": image_base64}))
