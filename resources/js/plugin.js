import Toastify from 'toastify-js'
import "toastify-js/src/toastify.css"
import AirDatepicker from 'air-datepicker';
import 'air-datepicker/air-datepicker.css';
import localeEn from 'air-datepicker/locale/en';
import localeJa from 'air-datepicker/locale/ja';
import 'flowbite';

window.AirDatepicker = AirDatepicker
window.localeEn = localeEn
window.localeJa = localeJa
window.Toastify = Toastify

const settings = {
    faceDetectionConfidence: 0.8,
    faceFPS: 30,
    handDetectionConfidence: 0.5,
    handFPS: 1,
    faceRecognizationFailCount: 3,
    timeLocale: "Jp",
    qrErrorAlertDuration: 3,
    qrErrorMessage: "未承認のQRコードです。",
    eventMessageDuration: 5,
}

window.localStorage.setItem("defaultSettings", JSON.stringify(settings))