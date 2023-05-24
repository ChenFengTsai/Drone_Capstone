import sys
sys.path.append('./')

import configparser
from djitellopy import Tello

from object_detection import Object_Tracking

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression, scale_coords
from utils.datasets import letterbox
from utils.plots import plot_one_box

def main(drone):
    
    # todo: object dection to find (bottle)
    ot = Object_Tracking(drone)
    #ot.initialize_drone()
    ot.track_object()
    print('object tracking done')

if  __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('yolov5/config.ini')
    wifi_name = config.get('wifi', 'wifi_name')
    wifi_password = config.get('wifi', 'wifi_password')
    ip = config.get('wifi', 'ip')
    
    # initilize the drone
    drone = Tello(ip)
    #drone.connect()
    #drone.streamon()
    
    main(drone)