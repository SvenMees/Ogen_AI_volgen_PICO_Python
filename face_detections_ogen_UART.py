import cv2
import datetime
import imutils
import numpy as np
import serial.tools.list_ports
import pandas as pd

datacsvX = pd.read_csv("conversieX.csv")
datacsvY = pd.read_csv("conversieY.csv")
import seaborn as sb
import seaborn as sa


X = datacsvX["X"]
X1 = datacsvX["X1"]
Y = datacsvY["Y"]
Y1 = datacsvY["Y1"]
X_prossesd = X.values.reshape(-1,1)
X1_prossesd = X1.values.reshape(-1,1)
Y_prossesd = Y.values.reshape(-1,1)
Y1_prossesd = Y1.values.reshape(-1,1)


from sklearn.linear_model import LinearRegression

modelX = LinearRegression()
modelX.fit(X_prossesd, X1_prossesd)
modelY = LinearRegression()
modelY.fit(Y_prossesd,Y1_prossesd)


testke =471
trasholf = 2

voorspellingX = int (modelX.predict([[testke]]))
voorspellingY = int (modelY.predict([[testke]]))

print(f"{testke} omzettin is nu=  {voorspellingX}")
print(f"{testke} omzettin is nu=  {voorspellingY}")

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []
for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))

val = input("select Port : COM")


for x in range(0, len(portList)):
    if portList[x].startswith("COM"+str(val)):
        portVar = "COM" + str(val)
        print(portVar)

serialInst.bautrate = 9600
serialInst.port = portVar
serialInst.open()

protopath = "deploy.prototxt"
modelpath = "res10_300x300_ssd_iter_140000.caffemodel"
detector = cv2.dnn.readNetFromCaffe(prototxt=protopath, caffeModel=modelpath)
# Only enable it if you are using OpenVino environment
# detector.setPreferableBackend(cv2.dnn.DNN_BACKEND_INFERENCE_ENGINE)
# detector.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def main():
    cap = cv2.VideoCapture(0)

    fps_start_time = datetime.datetime.now()
    fps = 0
    total_frames = 0
    cX=0
    cY=0
    cxx=0
    cyy=0

    while True:
        
        ret, frame = cap.read()
      #  frame = cv2.flip(frame,2)
        frame = imutils.resize(frame, width=500)
        total_frames = total_frames + 1
        
        (H, W) = frame.shape[:2]

        face_blob = cv2.dnn.blobFromImage(cv2.resize(frame, (500, 500)), 1.0, (250, 250), (104.0, 177.0, 123.0), False, False)

        detector.setInput(face_blob)
        face_detections = detector.forward()
        
        for i in np.arange(0, face_detections.shape[2]):
            confidence = face_detections[0, 0, i, 2]
            if confidence > 0.5:

                face_box = face_detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = face_box.astype("int")

                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)
                #cX = int (model.predict([[int((startX + endX) / 2.0)]]))
                cX = int((startX + endX) / 2.0)
                #cY = int (model.predict([[int((startY + endY) / 2.0)]]))
                cY = int((startY + endY) / 2.0)
        fps_end_time = datetime.datetime.now()
        time_diff = fps_end_time - fps_start_time
        if time_diff.seconds == 0:
            fps = 0.0
        else:
            fps = (total_frames / time_diff.seconds)

        fps_text = "FPS: {:.2f}".format(fps)
        fps_text2 = "A{}A{}A\n".format(int (modelY.predict([[cY]])),int (modelX.predict([[cX]])))

        cv2.putText(frame, fps_text, (5, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
        cv2.putText(frame, fps_text2, (15, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
        cv2.imshow("Application", frame)
        
        if cX > cxx +trasholf or cX < cxx -trasholf or cY > cyy +trasholf or cY < cyy -trasholf:
            serialInst.write(fps_text2.encode('utf-8'))
            print(fps_text2.encode('utf-8'))
        

        cyy = cY   
        cxx = cX
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    cv2.destroyAllWindows()


main()
