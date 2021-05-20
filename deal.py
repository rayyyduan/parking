# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import cv2
import os
import numpy as np
import photoWindow

# 初始化参数
confThreshold = 0.5  # 置信度阈值
nmsThreshold = 0.4  # 非最大抑制阈值
inpWidth = 416  # 网络输入图像的宽度
inpHeight = 416  # 网络输入图像的高度
index = 'index.txt'
coco = "darknet/data/coco.names"


# 检测车辆
def extract_car(image_path):
    image = cv2.imread(image_path)
    (H, W) = image.shape[:2]

    # 仅确定我们从YOLO需要的输出图层名称
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    # 从输入图像构造一个Blob，然后执行正向
    # 通过YOLO对象检测器，为bounding boxes提供了关联概率
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (inpWidth, inpHeight), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    boxes = []
    confidences = []
    classIDs = []
    # 循环遍历每个图层输出
    for output in layerOutputs:
        # 遍历每个检测
        for detection in output:
            # 提取当前物体检测的类别ID和置信度（即概率）
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]

            # 通过确保检测到的概率大于最小概率来滤除弱预测
            if confidence > confThreshold:
                # 将边框的坐标相对于图像的大小向后缩放
                # YOLO实际上返回边框的中心（x，y）坐标，然后是边框的宽度和高度
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")

                # 使用中心（x，y）坐标导出边界框的左上角和左上角
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))

                # 更新边界框坐标列表，置信度和类ID列表
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID)
    # 应用非最大值抑制来抑制弱的重叠边界框
    idxs = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    # 确保至少有一个检测到
    if len(idxs) > 0:
        # 循环遍历我们保存的索引
        for i in idxs.flatten():
            # 提取边界框坐标
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            # if x in range(gBeginX, gBeginY) and y in range(gBeginX, gBeginY) and classes[classIDs[i]] in ['car', 'truck']:
            if x in range(180, 210) and y in range(180, 210) and classes[classIDs[i]] in ['car', 'truck']:
                # 从图像中提取汽车
                car = image[y:y + h, x:x + w]
                # cv2.imwrite('./car/'+image_path[6:], car)
                # print('car detected!')
                return extract_features(car)

        # print('no car detected!')
        return False


# 提取特征
def extract_features(image):
    # 启动SIFT检测器
    sift = cv2.xfeatures2d.SIFT_create()

    # 使用SIFT查找关键点和描述符
    kp, des = sift.detectAndCompute(image, None)

    return (kp, des)


# 匹配提取的特征
def extract_features_matching(feature, matching):
    if not feature or not matching:
        return False

    # 使用SIFT查找关键点和描述符
    kp1, des1 = feature[0], feature[1]
    kp2, des2 = matching[0], matching[1]

    # FLANN参数
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)  # 或通过空字典

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # 根据Lowe的比率测试存储所有符合条件的匹配项。
    good = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good.append(m)

    MIN_MATCH_COUNT = 3
    if len(good) > MIN_MATCH_COUNT:
        # print('... same car!')
        return True
    else:
        # print('... different car!')
        return False


def deal(beginX, beginY, endX, endY, occupyTime):
    global gBeginX, gBeginY, gEndX, gEndY, gOccupyTime
    gBeginX = beginX
    gBeginY = beginY
    gEndX = endX
    gEndY = endY
    gOccupyTime = int(occupyTime)
    # with open(index) as f:
    #     data = f.readlines()
    # for i in range(2000, 8000, 60):
    #     timestamp = data[i][:-1]
    #
    #     # 读取视频
    #     cam = cv2.VideoCapture('https://hiring.verkada.com/video/' + timestamp)
    #     print('downloading https://hiring.verkada.com/video/' + timestamp)
    #     try:
    #         # 创建image文件夹
    #         if not os.path.exists('image'):
    #             os.makedirs('image')
    #             # 如果未创建成功则报错
    #     except OSError:
    #         print('Error: Creating directory of image')
    #
    #         # 读取frame
    #     ret, frame = cam.read()
    #
    #     if ret:
    #         # 如果仍有视频则继续创建图像
    #         name = './image/' + timestamp[:-3] + '.jpg'
    #         print('extracting image...wrote ' + name)
    #
    #         # 写入提取到的图像
    #         cv2.imwrite(name, frame)
    #
    #         # 完成后释放所有空间
    #     cam.release()
    #     # cv2.destroyAllWindows()

    # 加载类名
    global classes
    with open(coco, 'rt') as f:
        classes = f.read().rstrip('\n').split('\n')

    # 加载在COCO训练集上训练的预训练集YOLO对象检测器（80类）
    print('loading YOLO...')
    global net
    net = cv2.dnn.readNetFromDarknet('darknet/cfg/yolov3.cfg', 'yolov3.weights')
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    # 将preferable target设置为cv.dnn.DNN_TARGET_OPENCL以在GPU上运行它
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    with open(index) as f:
        data = f.readlines()

    images_path = 'image/'
    files = [os.path.join(images_path, p) for p in sorted(os.listdir(images_path))]

    # 观察到的停车位的初始状态
    occupied = False
    # 最初停在该地点的汽车的特征
    occupied_feature = None
    start = None

    for i in range(1, len(files)):
        cur_car_feature = extract_car(files[i])
        if cur_car_feature:  # 如果在当前img的该地点发现了一辆汽车
            if not occupied:  # 如果该地点未被占用
                occupied = True
                occupied_feature = cur_car_feature
                start = files[i][6:-4]
                print('found car at ' + start, end='')

            # 如果位置被占用，则比较这两辆车以检查它们是否相同
            else:
                # 如果不是同一辆车，计算停车时间
                if not extract_features_matching(cur_car_feature, occupied_feature):
                    duration = int((int(files[i][6:-4]) - int(start)) / 60)
                    print(' parked until ' + files[i - 1][6:-4] + '(%s minutes).' % duration)
                    if gOccupyTime < duration:
                        print('！！！车辆违规占用消防车道，已拍照留证！！！')
                        image = cv2.imread('image/' + start + '.jpg')
                        print('image/' + start + '.jpg')
                        name = 'output/' + start + '-%smin.jpg' % duration
                        cv2.imwrite(name, image)
                        print('...wrote output/' + start + '-%smin.jpg' % duration)
                    start = files[i][6:-4]
                    print('found car at ' + start, end='')
                occupied_feature = cur_car_feature
        # 如果在当前img的该位置没有找到汽车
        else:
            if occupied:
                duration = int((int(files[i][6:-4]) - int(start)) / 60)
                print(' parked until ' + files[i - 1][6:-4] + '(%s minutes).' % duration)
                if gOccupyTime < duration:
                    print('！！！车辆违规占用消防车道，已拍照留证！！！')
                    image = cv2.imread('image/' + start + '.jpg')
                    print('image/' + start + '.jpg')
                    name = 'output/' + start + '-%smin.jpg' % duration
                    cv2.imwrite(name, image)
                    print('...wrote output/' + start + '-%smin.jpg' % duration)

                occupied_feature = None
                start = None
                occupied = False
    photoWindow.showPhoto()


# 测试用
if __name__ == '__main__':
    deal(1, 1, 1, 1, 1)
