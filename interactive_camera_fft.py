import numpy as np
import cv2

def myfunc(i):
    pass #do nothing

# calclate sigmoid function
def sig(i, x):
    return 1 / (1 + np.exp(- i * x))

# change contrast by using sigmoid function
def changeGrayContrast(i, x):
    MAX = 1
    if i != 0:
        x = x / 255 * MAX
        x = (sig(i, x - MAX / 2) - sig(i, 0 - MAX / 2)) * (255 / (sig(i, MAX - MAX / 2) - sig(i, 0 - MAX / 2)))
    return x

# x.shape == (*,*,3)
def changeContrast(i, x):
    x[:,:,0] = changeGrayContrast(i, x[:,:,0])
    x[:,:,1] = changeGrayContrast(i, x[:,:,1])
    x[:,:,2] = changeGrayContrast(i, x[:,:,2])
    return x
    
def gammaCorrect(r, x):
    if r != 0:
        x = 255 * np.power(x / 255, 1 / r)
    else:
        x = 255 * np.power(x / 255, 1 / 0.001)
    return x

def gaussian(r, x, y):
    g = 1
    if np.square(x) + np.square(y) > r * 10000:
        g = 0
    return g


def lowPassFilter(r, x):
    h, w = x[:,:,0].shape
    fx = np.zeros((h,w,3), dtype=complex)
    fx[:,:,0] = np.fft.fft2(x[:,:,0])
    fx[:,:,1] = np.fft.fft2(x[:,:,1])
    fx[:,:,2] = np.fft.fft2(x[:,:,2])
    fx[:,:,0] = np.fft.fftshift(fx[:,:,0])
    fx[:,:,1] = np.fft.fftshift(fx[:,:,1])
    fx[:,:,2] = np.fft.fftshift(fx[:,:,2])
    for j in range(h):
        for i in range(w):
            g = gaussian(r, i, j)
            fx[j,i,0] = g * fx[j,i,0]
            fx[j,i,1] = g * fx[j,i,1]
            fx[j,i,2] = g * fx[j,i,2]
    fx[:,:,0] = np.fft.fftshift(fx[:,:,0])
    fx[:,:,1] = np.fft.fftshift(fx[:,:,1])
    fx[:,:,2] = np.fft.fftshift(fx[:,:,2])
    x[:,:,0] = np.uint8(np.fft.ifft2(fx[:,:,0]).real)
    x[:,:,1] = np.uint8(np.fft.ifft2(fx[:,:,1]).real)
    x[:,:,2] = np.uint8(np.fft.ifft2(fx[:,:,2]).real)
    return x

cv2.namedWindow('interactive-camera') # create win with win name

cv2.createTrackbar('contrast', # name of value
                   'interactive-camera', # win name
                   0, # min
                   9, # max
                   myfunc) # callback func

cv2.createTrackbar('hue', # name of value
                   'interactive-camera', # win name
                   10, # min
                   100, # max
                   myfunc) # callback func

cv2.createTrackbar('saturation', # name of value
                   'interactive-camera', # win name
                   10, # min
                   100, # max
                   myfunc) # callback func

cv2.createTrackbar('value', # name of value
                   'interactive-camera', # win name
                   10, # min
                   100, # max
                   myfunc) # callback func

cv2.createTrackbar('gaussian', # name of value
                   'interactive-camera', # win name
                   50, # min
                   50, # max
                   myfunc) # callback func



cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


while(True):

    ret, frame = cap.read()
    if not ret: continue
    
    a = cv2.getTrackbarPos('contrast',  # get the value
                       'interactive-camera')  # of the win
                       
    h = cv2.getTrackbarPos('hue',  # get the value
                           'interactive-camera')  # of the win
    s = cv2.getTrackbarPos('saturation',  # get the value
                           'interactive-camera')  # of the win
    v = cv2.getTrackbarPos('value',  # get the value
                       'interactive-camera')  # of the win
    r = cv2.getTrackbarPos('gaussian',  # get the value
                       'interactive-camera')  # of the win
    
    # change contrast
    if a != 0:
        frame = changeContrast(a, frame)
    
    # change hue, saturation and value
    frame_hls = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    if h != 10:
        frame_hls[:,:,0] = gammaCorrect(h / 10, frame_hls[:,:,0])
    if s != 10:
        frame_hls[:,:,1] = gammaCorrect(s / 10, frame_hls[:,:,1])
    if v != 10:
        frame_hls[:,:,2] = gammaCorrect(v / 10, frame_hls[:,:,2])
    frame = cv2.cvtColor(frame_hls, cv2.COLOR_HSV2RGB)
    
    # low pass filter
    if r != 50:
        frame = lowPassFilter(r, frame)

    cv2.imshow('interactive-camera', frame)  # show in the win

    k = cv2.waitKey(1)
    if k == ord('q') or k == 27:
        break



cap.release()
cv2.destroyAllWindows()
