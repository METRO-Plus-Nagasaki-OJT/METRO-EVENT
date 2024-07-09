import { drawLandmarks, drawRectangle } from '@mediapipe/drawing_utils';
import { FaceDetection } from '@mediapipe/face_detection';
import { FaceMesh } from '@mediapipe/face_mesh';
import { Hands } from '@mediapipe/hands';

window.FaceDetection = FaceDetection
window.Hands = Hands
window.FaceMesh = FaceMesh
window.drawRectangle = drawRectangle
window.drawLandmarks = drawLandmarks