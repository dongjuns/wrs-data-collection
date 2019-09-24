import tkinter as tk
from PIL import Image, ImageTk
import os
import time


class Annotater:
    def __init__(self, obj_list, img_list, out_dir, size):
        self.img_list = img_list
        self.img_id = -1
        self.obj_list = obj_list
        self.obj_id = 0

        self.out_dir = out_dir
        self.size = size

        self.orientation = None
        self.xs = None
        self.ys = None

        self.img = None
        self.img_path = None

        self.m = tk.Tk()
        self.m.title("Paint mask using ovals")
        self.c = tk.Canvas(
            self.m,
            width=size[0],
            height=size[1]
        )
        self.c.pack(expand=tk.YES, fill=tk.BOTH)
        self.c.bind("<Motion>", self.mouse_move)
        self.c.bind("<B1-ButtonRelease>", self.mouse_button)
        self.c.bind("<ButtonPress>", self.mouse_button)
        self.line = None

        self.next(do_pause=False)
        tk.mainloop()

    def get_out_fname(self):
        fname = self.img_path.split('/')[-1][:-4] + "_{}".format(self.obj_id)
        return self.out_dir + "/" + fname

    def next(self, do_pause=True):
        while not self._next(do_pause):
            pass

    def _next(self, do_pause=True):
        self.c.delete("all")
        self.img_id += 1
        if self.img_id == len(self.img_list):
            self.img_id = 0
            self.obj_id += 1
            if self.obj_id == len(self.obj_list):
                self.m.destroy()
                return True
            if do_pause:
                time.sleep(1)
                print("!!!!NEW OBJECT!!!")
                time.sleep(1)

        self.orientation = 0
        self.xs, self.ys = [], []
        self.img_path = self.img_list[self.img_id]
        if os.path.exists(self.get_out_fname()):
            return False
        percentage = self.obj_id * len(self.img_list) + self.img_id
        percentage /= len(self.img_list) * len(self.obj_list)
        print("{}% -- {} -- OBJ: {}, IMG: {}".format(int(percentage * 100), self.img_id, self.obj_id,
                                                     self.img_path.split('/')[-1]))
        self.img = ImageTk.PhotoImage(Image.open(self.img_path))
        self.c.create_image(self.size[0] // 2, self.size[1] // 2, image=self.img)
        self.c.update()
        return True

    def draw_line(self, x, y, color="black"):
        dx, dy = (0, 2000) if self.vertical() else (2000, 0)
        return self.c.create_line(x - dx, y - dy, x + dx, y + dy, fill=color, width=2)

    def vertical(self):
        return self.orientation < 2 if self.img_id % 2 == 0 else self.orientation > 1

    def mouse_move(self, e):
        if self.line:
            self.c.delete(self.line)
        self.line = self.draw_line(e.x, e.y, color='red')

    def mouse_button(self, e):
        (self.xs if self.vertical() else self.ys).append(e.x if self.vertical() else e.y)
        self.draw_line(e.x, e.y, color='blue')
        self.orientation += 1
        if self.orientation == 4:
            assert len(self.ys) == len(self.xs) == 2
            xmin, xmax = min(self.xs), max(self.xs)
            ymin, ymax = min(self.ys), max(self.ys)

            with open(self.get_out_fname(), 'w+') as f:
                f.write('{},{},{},{}\n'.format(xmin, ymin, xmax, ymax))
            self.next()


def main():
    root_dir = "."
    rgb_dir = root_dir + '/dataset'
    obj_dir = root_dir + '/obj_imgs'
    out_dir = root_dir + '/annotations'
    rgb_list = sorted([rgb_dir + '/' + p for p in os.listdir(rgb_dir)])
    obj_list = sorted([obj_dir + '/' + p for p in os.listdir(obj_dir)])

    Annotater(obj_list, rgb_list, out_dir, (1920, 1200))


if __name__ == '__main__':
    main()
