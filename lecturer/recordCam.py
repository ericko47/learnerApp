import cv2


class VideoCamera:
    @staticmethod
    def record():
        cam = cv2.VideoCapture(0)
        cv2.namedWindow('CAPTURE', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('CAPTURE', 800, 600)
        fps = 1000/20
        while True:
            ret, frame = cam.read()
            cv2.putText(frame, 'press q to quit camera', (10, 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 7, 0))
            cv2.imshow("CAPTURE", frame)
            if cv2.waitKey(int(fps)) & 0xFF == ord('q'):
                break
        cam.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    VideoCamera().record()
