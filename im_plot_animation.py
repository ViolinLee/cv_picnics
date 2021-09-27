import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation
from glob import glob
from tqdm import tqdm


class DataParser(object):
    def __init__(self):
        pass

    def rgbd_from_npz(self, npz_data):
        depth_pix, color_pix = npz_data['depthPix'], npz_data['colorPix']
        return depth_pix, color_pix

    def pix_range_adjust(self, src_data, src_region, dst_region):
        return np.interp(src_data, src_region, dst_region)


if __name__ == "__main__":
    data_parser = DataParser()

    # prepare data stream
    dir_path = r"target_dir\*"
    file_paths = glob(dir_path)[:100]
    color_frames = []
    depth_frame_ms = []
    for i, file_path in tqdm(enumerate(file_paths)):
        data = np.load(file_path, allow_pickle=True)
        depth_frame, color_frame = data_parser.rgbd_from_npz(data)
        color_frames.append(color_frame)
        depth_frame_adjusted = data_parser.pix_range_adjust(depth_frame, [0, np.max(depth_frame)], [0, 255]).astype(np.uint8)
        depth_frame_ms.append(np.round(np.mean(depth_frame[372:447, 159:214]) / 10000, 4))
        cv2.imshow("adjusted depth", depth_frame_adjusted)
        if cv2.waitKey(100) == ord("q"):
            break

    # set up the figure, create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1)
    # initialize two line objects (one in each axes)
    line, = ax1.plot([], [], lw=2, color='r')
    img = ax2.imshow(color_frames[0])
    # the same axes initializations as before (just now we do it for both of them)
    ax1.set_ylim(np.mean(depth_frame_ms)*0.99, np.mean(depth_frame_ms)*1.01)
    ax1.set_xlim(0, len(depth_frame_ms))
    xdata, ydata = [], []

    def update(n):
        xdata.append(n)
        ydata.append(depth_frame_ms[n])
        print(n, depth_frame_ms[n])
        line.set_data(xdata, ydata)

        img.set_data(color_frames[n])
        plt.show()
        return line, img

    ani = animation.FuncAnimation(fig, update, frames=len(color_frames), blit=True)
    ani.save('sin_dot.gif', writer='imagemagick', fps=10)
