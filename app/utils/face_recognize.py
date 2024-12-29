import cv2
import numpy as np
from flask import jsonify

import app.utils.utils as utils
from app.utils.net.inception import InceptionResNetV1
from app.utils.net.mtcnn import mtcnn
from PIL import Image, ImageDraw, ImageFont


class Face_rec():
    _instance = None  # 存储唯一实例

    def __new__(cls, *args, **kwargs):
        # 如果实例已经存在，则直接返回该实例
        if not cls._instance:
            cls._instance = super(Face_rec, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            # -------------------------#
            #   创建mtcnn的模型
            #   用于检测人脸
            # -------------------------#
            self.mtcnn_model = mtcnn()
            self.threshold = [0.5, 0.6, 0.8]

            # -----------------------------------#
            #   载入facenet
            #   将检测到的人脸转化为128维的向量
            # -----------------------------------#
            self.facenet_model = InceptionResNetV1()
            model_path = 'D:/code/python/faceweb/app/utils/model_data/facenet_keras.h5'
            self.facenet_model.load_weights(model_path)

    def recognize(self, img, queryed_features):
        stored_features = []
        stored_names = []
        for queried_feature in queryed_features:
            stored_features.append(np.frombuffer(queried_feature.feature, dtype=np.float32))
            stored_names.append(queried_feature.students.name)

        # 提取人脸特征
        face_features, rectangles = self.get_feature(img)

        if len(face_features) == 0:
            return jsonify({"message": "图片未识别到人脸特征！"}), 400

        recognized_names = []

        for feature in face_features:
            # -------------------------------------------------------#
            #   取出一张脸并与数据库中所有的人脸进行对比，计算得分
            # -------------------------------------------------------#
            matches = utils.compare_faces(stored_features, feature, tolerance=0.9)
            # -------------------------------------------------------#
            #   找出距离最近的人脸
            # -------------------------------------------------------#
            face_distances = utils.face_distance(stored_features, feature)
            # -------------------------------------------------------#
            #   取出这个最近人脸的评分
            # -------------------------------------------------------#
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                recognized_names.append(stored_names[best_match_index])
            else:
                recognized_names.append("陌生人")

        rectangles = rectangles[:, 0:4]

        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)

        font_style = ImageFont.truetype("NotoSansSC-Light.ttf", 50)

        for (left, top, right, bottom), name in zip(rectangles, recognized_names):
            draw.rectangle([left, top, right, bottom], fill=None, outline=None, width=2)
            draw.text((left, top + 3), name, (0, 255, 0), font=font_style)

        return img, recognized_names

    def get_feature(self, img):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        height, width, _ = np.shape(img)
        draw_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # --------------------------------#
        #   检测人脸
        # --------------------------------#
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return

        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, [0, 2]] = np.clip(rectangles[:, [0, 2]], 0, width)
        rectangles[:, [1, 3]] = np.clip(rectangles[:, [1, 3]], 0, height)

        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            # ---------------#
            #   截取图像
            # ---------------#
            landmark = np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])
            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            # -----------------------------------------------#
            #   利用人脸关键点进行人脸对齐
            # -----------------------------------------------#
            crop_img, _ = utils.Alignment_1(crop_img, landmark)
            crop_img = np.expand_dims(cv2.resize(crop_img, (160, 160)), 0)

            face_encoding = utils.calc_128_vec(self.facenet_model, crop_img)
            face_encodings.append(face_encoding)
        return face_encodings, rectangles
