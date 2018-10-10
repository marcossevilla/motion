import cv2, time, pandas
from datetime import datetime

first_frame = None
status_list = [None, None]
times = []
df = pandas.DataFrame(columns=["Start", "End"])
video = cv2.VideoCapture(0)

while True:

    check, frame = video.read() # read returns a boolean and a numpy array
    status = 0 # status of movement, 0 means false
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # transforming to gray
    gray = cv2.GaussianBlur(gray, (21,21), 0) # the image is easier to work with

    if first_frame is None:
        first_frame = gray
        continue

    # delta frame superposes both first still frame and the gray actual frame
    delta_frame = cv2.absdiff(first_frame, gray)
    # threshold the delta_frame to 
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    # smooth the image with dilate method, more iterations = smoother image
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # finding contours
    (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # iterate over contours
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        status = 1 # status of movement
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    status_list.append(status)
    status_list = status_list[-2:]

    if (status_list[-1] == 1 and status_list[-2] == 0) or (status_list[-1] == 0 and status_list[-2] == 1):
        times.append(datetime.now())

    # cv2.imshow("Gray", gray)
    # cv2.imshow("Delta", delta_frame)
    cv2.imshow("Threshold", thresh_frame)
    cv2.imshow("Color frame", frame)

    key = cv2.waitKey(1)

    # gets key input, 'q' breaks the loop
    if key == ord('q'):
        if status==1:
            times.append(datetime.now())
        break

# append data to dataframe
for i in range(0, len(times), 2):
    df = df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)

# export dataframe
df.to_csv("Times.csv")

video.release()
cv2.destroyAllWindows()