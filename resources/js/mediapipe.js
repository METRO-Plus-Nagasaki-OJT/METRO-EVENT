
import { FaceDetection } from '@mediapipe/face_detection';
import { Hands } from '@mediapipe/hands';
import jsQR from "jsqr";
import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"

window.FaceDetection = FaceDetection
window.Hands = Hands
window.jsQR = jsQR
window.Toastify = Toastify