import cv2, time
from AIMakeup import Makeup

if __name__ == '__main__':
    cap = cv2.VideoCapture("output.mp4")  # 输入视频地址
    mu = Makeup()
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    videoWriter = cv2.VideoWriter('saveVideo.avi', fourcc, fps, (w, h))  # 最后一个是保存图片的尺寸
    flag = 0
    time_start = time.time_ns()

    while (cap.isOpened()):
        loop_time_start = time.time()
        flag += 1
        # get a frame
        ret, frame = cap.read()
        # show a frame
        # cv2.imshow("capture", frame)
        # 整体双边滤波
        frame = cv2.bilateralFilter(frame, 3, 75, 75)
        im, temp_bgr, faces = mu.read_and_mark(frame)

        print(faces)
        if (len(faces) >= 1):
            print('美化了第 {} 帧'.format(flag))
            for face in faces:
                face.whitening()
                face.smooth(0.9)
                face.organs['forehead'].whitening()
                face.organs['forehead'].smooth(0.7)
                face.organs['mouth'].brightening()
                face.organs['mouth'].smooth(0.7)
                face.organs['mouth'].whitening()
                face.organs['left eye'].whitening()
                face.organs['right eye'].whitening()
                face.organs['left eye'].sharpen()
                face.organs['right eye'].sharpen()
                face.organs['left eye'].smooth()
                face.organs['right eye'].smooth()
                face.organs['left brow'].whitening()
                face.organs['right brow'].whitening()
                face.organs['left brow'].sharpen()
                face.organs['right brow'].sharpen()
                face.organs['nose'].whitening()
                face.organs['nose'].smooth(0.9)
                face.organs['nose'].sharpen()
                face.sharpen()
            but_time_end = time.time()
            print('这个美化花了：', (but_time_end - loop_time_start) * 1000, '毫秒')
        print('打印了第 {} 帧'.format(flag))
        loop_time_end = time.time()
        videoWriter.write(im)
        print('这个循环花了：', (loop_time_end - loop_time_start) * 1000, '毫秒')
    videoWriter.release()
    time_end = time.time()
    print('结束')
    print('总共花了', time_end - time_start, 's')
