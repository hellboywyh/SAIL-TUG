#----------------description----------------# 
# Author       : Yanhong Wang
# E-mail       : yhwang18@fudan.edu.cn
# Company      : IBICAS, Fudan University
# Date         : 2022-07-07 12:07:07
# LastEditors  : Yanhong Wang
# LastEditTime : 2022-07-07 18:03:46
# FilePath     : \SAIL-TUG\vis_images.py
# Description  : 
#-------------------------------------------# 
import json
import cv2
import os
from fn import vis_frame

with open("sail-color/public/annotations/keyPoints.json","r") as f:
    data_json = json.load(f)
    imgnames = data_json["imgname"]
    bndboxes = data_json["bndbox"]
    parts = data_json["part"]
    # print(len(imgnames))
    # print(len(bndboxes))
    # print(len(parts))
    for i in range(35646):
        im_res = {}
        im_res['imgname'] = imgnames[i]
        human = {}
        human['keypoints'] = parts[i]
        human['kp_score'] = [1 for i in range(17)]
        im_res['result'] = [human]
        ori_img = cv2.imread("sail-color/public/images_test/"+im_res['imgname'])
        img = vis_frame(ori_img, im_res)
        cv2.imshow("骨骼图", img)
        cv2.waitKey(0)