import os, imageio, shutil

def save_video(filename="map"):
    png_dir = "Snaps"
    images = []
    for file in sorted(os.listdir(png_dir)):
        fpath = os.path.join(png_dir, file)
        images.append(imageio.imread(fpath))
    imageio.mimsave(f"coverage_{filename}.gif", images)
    shutil.rmtree(png_dir)