#----------------description----------------# 
# Author       : Yanhong Wang
# E-mail       : yhwang18@fudan.edu.cn
# Company      : IBICAS, Fudan University
# Date         : 2022-07-07 18:04:01
# LastEditors  : Yanhong Wang
# LastEditTime : 2022-07-07 18:04:29
# FilePath     : \SAIL-TUG\fn.py
# Description  : 
#-------------------------------------------# 
import cv2
import numpy as np
import math

def vis_frame(frame, im_res):
    l_pair = [
        (0, 1), (0, 2), (1, 3), (2, 4),  # Head
        (5, 6), (5, 7), (7, 9), (6, 8), (8, 10),
        (17, 11), (17, 12),  # Body
        (11, 13), (12, 14), (13, 15), (14, 16)
    ]

    p_color = [(0, 255, 255), (0, 191, 255),(0, 255, 102),(0, 77, 255), (0, 255, 0), #Nose, LEye, REye, LEar, REar
                (77,255,255), (77, 255, 204), (77,204,255), (191, 255, 77), (77,191,255), (191, 255, 77), #LShoulder, RShoulder, LElbow, RElbow, LWrist, RWrist
                (204,77,255), (77,255,204), (191,77,255), (77,255,191), (127,77,255), (77,255,127), (0, 255, 255)] #LHip, RHip, LKnee, Rknee, LAnkle, RAnkle, Neck
    line_color = [(0, 215, 255), (0, 255, 204), (0, 134, 255), (0, 255, 50), 
                (77,255,222), (77,196,255), (77,135,255), (191,255,77), (77,255,77), 
                (77,222,255), (255,156,127), 
                (0,127,255), (255,127,77), (0,77,255), (255,77,36)]
    
    im_name = im_res['imgname'].split('/')[-1]
    img = frame
    height,width = img.shape[:2]
    img = cv2.resize(img,(int(width/2), int(height/2)))
    for human in im_res['result']:
        part_line = {}
        kp_preds = human['keypoints']
        kp_scores = human['kp_score']
        # kp_preds = torch.cat((kp_preds, torch.unsqueeze((kp_preds[5,:]+kp_preds[6,:])/2,0)))
        # kp_scores = torch.cat((kp_scores, torch.unsqueeze((kp_scores[5,:]+kp_scores[6,:])/2,0)))
        # Draw keypoints
        for n in range(len(kp_scores)):
            if kp_scores[n] <= 0.05:
                continue
            cor_x, cor_y = int(kp_preds[n][0]), int(kp_preds[n][1])
            part_line[n] = (int(cor_x/2), int(cor_y/2))
            bg = img.copy()
            cv2.circle(bg, (int(cor_x/2), int(cor_y/2)), 2, p_color[n], -1)
            # Now create a mask of logo and create its inverse mask also
            transparency = max(0, min(1, kp_scores[n]))
            img = cv2.addWeighted(bg, transparency, img, 1-transparency, 0)
        # Draw limbs
        for i, (start_p, end_p) in enumerate(l_pair):
            if start_p in part_line and end_p in part_line:
                start_xy = part_line[start_p]
                end_xy = part_line[end_p]
                bg = img.copy()

                X = (start_xy[0], end_xy[0])
                Y = (start_xy[1], end_xy[1])
                mX = np.mean(X)
                mY = np.mean(Y)
                length = ((Y[0] - Y[1]) ** 2 + (X[0] - X[1]) ** 2) ** 0.5
                angle = math.degrees(math.atan2(Y[0] - Y[1], X[0] - X[1]))
                stickwidth = (kp_scores[start_p] + kp_scores[end_p]) + 1
                polygon = cv2.ellipse2Poly((int(mX),int(mY)), (int(length/2), stickwidth), int(angle), 0, 360, 1)
                cv2.fillConvexPoly(bg, polygon, line_color[i])
                #cv2.line(bg, start_xy, end_xy, line_color[i], (2 * (kp_scores[start_p] + kp_scores[end_p])) + 1)
                transparency = max(0, min(1, 0.5*(kp_scores[start_p] + kp_scores[end_p])))
                img = cv2.addWeighted(bg, transparency, img, 1-transparency, 0)
    img = cv2.resize(img,(width,height),interpolation=cv2.INTER_CUBIC)
    return img
