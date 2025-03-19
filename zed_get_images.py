import pyzed.sl as sl
import cv2 as cv
import numpy as np
import time 

def main(cnt_max,mode):
    zed = sl.Camera()
    init_params = sl.InitParameters()
    '''
    调整分辨率,VGA:(376,672) HD720:(720,1280) HD1080:(1080,1920) HD2K:(1242,2208)
    帧率,VGA:100 HD720:60 HD1080:30 HD2K:15
    '''
    init_params.camera_resolution = sl.RESOLUTION.VGA
    init_params.camera_fps = 60
    init_params.camera_image_flip = sl.FLIP_MODE.OFF
    runtime_parameters = sl.RuntimeParameters()
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(-1)
    cnt = 0
    while True:
        img_l = sl.Mat()
        img_r = sl.Mat()
        depth = sl.Mat()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:

            zed.retrieve_image(img_l,sl.VIEW.LEFT)
            img_l_bgr = img_l.get_data()[:,:,:-1]    # img_rgb = cv.cvtColor(img_bgr, cv.COLOR_BGR2RGB)

            zed.retrieve_image(img_r,sl.VIEW.RIGHT)
            img_r_bgr = img_r.get_data()[:,:,:-1]

            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)
            
            
            cv.imshow('img',img_l_bgr)
            # cv.imshow('img_pair',np.hstack((img_l_bgr,img_r_bgr)))
            key = cv.waitKey(1)

            save_path = '/home/lvpin/Desktop/code/zed_get_images_svo/1'
            #连续保存图片
            if mode == 0:
                cv.imwrite(save_path+'/L/{}.png'.format(cnt),img_l_bgr)

                cv.imwrite(save_path+'/R/{}.png'.format(cnt),img_r_bgr)

                depth_data = depth.get_data() # mm单位
                h,w = depth_data.shape[0],depth_data.shape[1]
                for i in range(h):
                    for j in range(w):
                        if np.isnan(depth_data[i,j]) or np.isinf(depth_data[i,j]):
                            depth_data[i,j] = 0
                depth_save = depth_data.astype(np.float32)
                cv.imwrite(save_path+'/depth/{}.tiff'.format(cnt),depth_save) # cv.imread(save_path,cv.IMREAD_ANYDEPTH)

                cnt += 1
            elif mode == 1:
                if key == ord('s'):
                    cv.imwrite(save_path+'/L/{}.png'.format(cnt),img_l_bgr)

                    cv.imwrite(save_path+'/R/{}.png'.format(cnt),img_r_bgr)

                    depth_data = depth.get_data() # mm单位
                    h,w = depth_data.shape[0],depth_data.shape[1]
                    for i in range(h):
                        for j in range(w):
                            if np.isnan(depth_data[i,j]) or np.isinf(depth_data[i,j]):
                                depth_data[i,j] = 0
                    depth_save = depth_data.astype(np.float32)
                    cv.imwrite(save_path+'/depth/{}.tiff'.format(cnt),depth_save)

                    cnt += 1
            else:
                print('mode error')

            if cnt >= cnt_max:
                break
            if key == ord('q'):
                break
    cv.destroyAllWindows()
    zed.close()

if __name__ == "__main__":
    # 设定最大拍摄图片数量
    cnt_max = 1000000000
    # 设定保存模式,0:连续保存,1:手动按s保存
    # 设定相机分辨率和帧率、保存路径、拍摄时获取的数据
    mode = 1
    main(cnt_max,mode)
    