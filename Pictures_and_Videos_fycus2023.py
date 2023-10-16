#Códig para tomar fotos y vídeos espaciados en tiempo usando
#múltiples cámaras raspi y usb
#FYCUS 2023
#autor: Juan C.
#fecha: 16/09/2023

#LIBRERIAS
#RaspiCam
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
import time
#Usb cam & files creation
import os
import datetime
###########

first_directory = "/home/raspberryfycus/Desktop/Fotos_y_videos/"
os.chdir(first_directory)
foldername = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
#crear carpeta nueva donde guardar fotos y videos
os.mkdir(f"{foldername}")
#mover directorio de trabajo a carpeta nueva
directory = "/home/raspberryfycus/Desktop/Fotos_y_videos/{}".format(foldername)
os.chdir(directory)

#crear log de fallos
log_name = "{}_error_log.txt".format(foldername)
log_file = open(log_name,"w+")

n_pictures = range(5)


#bucle infinito

while True:
########################## RASPICAM ####################

    try:
        ########take a picture
        picam = Picamera2()
        #Raspicam config
        photo_config = picam.create_still_configuration(main={"size": (3280, 2464)})
        picam.configure(photo_config)
    
        picam.start()
        for n in n_pictures:
            time.sleep(2)
            photoname = datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg")
            picam.capture_file(photoname)
            time.sleep(5) #esperar 5 sec entre fotos
        picam.close()
    
    except:
        photoname = datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg")
        error_name = "{} pi photo failed".format(datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg"))
        log_file.write(error_name)
        log_file.write('\n')
############

    try:
        ##########make a video
        picam2 = Picamera2()
        video_config = picam2.create_video_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
        picam2.configure(video_config)

        encoder = H264Encoder(10000000)

        videoname = datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.h264")
        picam2.start_recording(encoder, videoname)
        time.sleep(30) #30 second video
        picam2.stop_recording()
        picam2.close()
    except:
        error_name = "{} pi video failed".format(datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg"))
        log_file.write(error_name)
        log_file.write('\n')
############

############
## USB PHOTO
    try:
        for n in n_pictures:
            usb_photo_input = "fswebcam -r 1920x1080 -S 3 --jpeg 50 --save {}/%Y-%m-%d-%H.%M.%S_usb.jpg".format(directory)
            os.system(usb_photo_input) # uses Fswebcam to take picture
            time.sleep(5) #esperar 5 sec entre fotos
    except:
        error_name = "{} usb photo failed".format(datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg"))
        log_file.write(error_name)
        log_file.write('\n')
    
############
## USB VIDEO
    try:
        usb_videoname = datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S_usbvideo.h264")
        usb_video_input = "ffmpeg -f v4l2 -t 00:00:30 -vcodec mjpeg -r 30 -video_size 1280x720 -i /dev/video0 {}/{}".format(directory,usb_videoname)
        os.system(usb_video_input)
    except:
        error_name = "{} usb video failed".format(datetime.datetime.now() .strftime ("%Y-%m-%d-%H.%M.%S.jpg"))
        log_file.write(error_name)
        log_file.write('\n')
    
    time.sleep(60) #esperar 1 minuto para repetir