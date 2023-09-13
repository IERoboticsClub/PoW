import torch
import timm
import einops
import tqdm
import cv2 as cv2
import numpy as np
import time
import os
import sys



# implementation idea:
# live tracking from the camera
# use the cotracker to track the object in the center of the image

# start building up a video buffer
# create a 7 second frame to shift every time the modelfinishes a prediction

# first test, record 5 second video, then run the model on it

def record_video():
    # record a 5 second video
    video = cv2.VideoCapture(0)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv2.CAP_PROP_FPS, 30)

    # create a buffer of 7 seconds
    buffer = []
    buffer_size = 7 * 30
    for i in range(buffer_size):
        ret, frame = video.read()
        buffer.append(frame)


    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter("buffer.mp4", fourcc, 30, (640, 480))

    for i in range(buffer_size):
        out.write(buffer[i])
    out.release()
    return "buffer.mp4", buffer


def load_video(pth):
    video = cv2.VideoCapture(pth)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video.set(cv2.CAP_PROP_FPS, 30)
    buffer = []
    while True:
        ret, frame = video.read()
        if not ret:
            break
        buffer.append(frame)
    return video, buffer

def main():
    # pth, vid_buffer = record_video()
    cotracker = torch.hub.load("facebookresearch/co-tracker", "cotracker_w8")

    print("model loaded")
    video, vid_buffer = load_video("demo.mp4")
    print("video loaded")
    video_torch = torch.from_numpy(np.array(vid_buffer)).permute(0, 3, 1, 2)[None].float()

    if torch.cuda.is_available():
        model = cotracker.cuda()
        video_torch = video_torch.cuda()

    tracks, visibility = cotracker(
        video_torch,
        grid_size=4,
        grid_query_frame=0,
        backward_tracking=False
    )

    print("model finished")
    print(tracks.shape)
    print(visibility.shape)

    # save the tracks
    np.save("tracks.npy", tracks.cpu().numpy())
    np.save("visibility.npy", visibility.cpu().numpy())

    # load the tracks



if __name__ == "__main__":
    main()
