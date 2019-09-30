# EsIOT mini project
## Smart traffic management system
A traffic signal control system made for RaspberryPi 3B+. Adaptive timer that changes depending on the vehicels on the road. Cameras are used to detect the number of vehicles waiting at the signal. Also captures the vehicles that jump the signals and stores their images on the firebase storage.<br>
Currently uses a simple static background subtraction to detect the vehicles instead of Haar classifiers.

### Libraries used:
- OpenCV
- Time & Datetime
- Numpy
- Google.cloud

### Screenshot

- <b> Vechicles getting captured in the ROI: </b>
<img src = "https://github.com/SAint7579/SmartTMS_IOT/blob/master/screen1.png"></img>

- <b> Images of jumpers on the cloud: </b>
<img src = "https://github.com/SAint7579/SmartTMS_IOT/blob/master/screen3.png"></img>

### Modules not added yet:
- Using SSD to detect the number plates of vehicles that violated the signal and translating it with tesseract engine.

