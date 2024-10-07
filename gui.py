"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""

import random
from tkinter import *
from tkinter.ttk import *


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_tabs_menu = self.__tk_tabs_menu(self)
        self.tk_label_frame_lw1wssni = self.__tk_label_frame_lw1wssni(
            self.tk_tabs_menu_0
        )
        self.tk_label_lw1wt1v6 = self.__tk_label_lw1wt1v6(self.tk_label_frame_lw1wssni)
        self.tk_input_package = self.__tk_input_package(self.tk_label_frame_lw1wssni)
        self.tk_button_save_path = self.__tk_button_save_path(
            self.tk_label_frame_lw1wssni
        )
        self.tk_input_path = self.__tk_input_path(self.tk_label_frame_lw1wssni)
        self.tk_select_box_download = self.__tk_select_box_download(
            self.tk_label_frame_lw1wssni
        )
        self.tk_check_button_downdload = self.__tk_check_button_downdload(
            self.tk_label_frame_lw1wssni
        )
        self.tk_label_frame_lw1wx3j1 = self.__tk_label_frame_lw1wx3j1(
            self.tk_tabs_menu_0
        )
        self.tk_button_download_start = self.__tk_button_download_start(
            self.tk_label_frame_lw1wx3j1
        )
        self.tk_button_open_path = self.__tk_button_open_path(
            self.tk_label_frame_lw1wx3j1
        )
        self.tk_button_download_infor = self.__tk_button_download_infor(
            self.tk_label_frame_lw1wx3j1
        )
        self.tk_label_frame_lw1xjzul = self.__tk_label_frame_lw1xjzul(
            self.tk_tabs_menu_1
        )
        self.tk_label_file_store = self.__tk_label_file_store(
            self.tk_label_frame_lw1xjzul
        )
        self.tk_label_target = self.__tk_label_target(self.tk_label_frame_lw1xjzul)
        self.tk_label_target_file = self.__tk_label_target_file(
            self.tk_label_frame_lw1xjzul
        )
        self.tk_input_file_store = self.__tk_input_file_store(
            self.tk_label_frame_lw1xjzul
        )
        self.tk_input_target = self.__tk_input_target(self.tk_label_frame_lw1xjzul)
        self.tk_input_target_file = self.__tk_input_target_file(
            self.tk_label_frame_lw1xjzul
        )
        self.tk_label_frame_lw1xmj4y = self.__tk_label_frame_lw1xmj4y(
            self.tk_tabs_menu_1
        )
        self.tk_button_install_start = self.__tk_button_install_start(
            self.tk_label_frame_lw1xmj4y
        )
        self.tk_button_install_infor = self.__tk_button_install_infor(
            self.tk_label_frame_lw1xmj4y
        )
        self.tk_button_install_uv = self.__tk_button_install_uv(
            self.tk_label_frame_lw1xmj4y
        )
        self.tk_label_lw2524gb = self.__tk_label_lw2524gb(self)
        self.tk_input_python_path = self.__tk_input_python_path(self)
        self.tk_label_frame_log = self.__tk_label_frame_log(self)
        self.tk_text_log = self.__tk_text_log(self.tk_label_frame_log)

    def __win(self):
        self.title("Python第三方库下载安装工具")
        # 设置窗口大小、居中
        width = 695
        height = 640
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        self.geometry(geometry)

        self.resizable(width=False, height=False)

    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""

        def show():
            if vbar:
                vbar.lift(widget)
            if hbar:
                hbar.lift(widget)

        def hide():
            if vbar:
                vbar.lower(widget)
            if hbar:
                hbar.lower(widget)

        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Enter>", lambda e: show())
        if vbar:
            vbar.bind("<Leave>", lambda e: hide())
        if hbar:
            hbar.bind("<Enter>", lambda e: show())
        if hbar:
            hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())

    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor="ne")

    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor="sw")

    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)

    def __tk_tabs_menu(self, parent):
        frame = Notebook(parent)
        self.tk_tabs_menu_0 = self.__tk_frame_menu_0(frame)
        frame.add(self.tk_tabs_menu_0, text="--在线-下载 --")
        self.tk_tabs_menu_1 = self.__tk_frame_menu_1(frame)
        frame.add(self.tk_tabs_menu_1, text="--离线-安装--")
        frame.place(x=0, y=0, width=685, height=290)
        return frame

    def __tk_frame_menu_0(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=685, height=290)
        return frame

    def __tk_frame_menu_1(self, parent):
        frame = Frame(parent)
        frame.place(x=0, y=0, width=685, height=290)
        return frame

    def __tk_label_frame_lw1wssni(self, parent):
        frame = LabelFrame(
            parent,
            text="输入",
        )
        frame.place(x=0, y=0, width=670, height=110)
        return frame

    def __tk_label_lw1wt1v6(self, parent):
        label = Label(
            parent,
            text="第三方库名",
            anchor="center",
        )
        label.place(x=0, y=0, width=80, height=30)
        return label

    def __tk_input_package(self, parent):
        ipt = Entry(
            parent,
        )
        ipt.place(x=100, y=0, width=320, height=30)
        return ipt

    def __tk_button_save_path(self, parent):
        btn = Button(
            parent,
            text="保存路径",
            takefocus=False,
        )
        btn.place(x=0, y=50, width=80, height=30)
        return btn

    def __tk_input_path(self, parent):
        ipt = Entry(
            parent,
        )
        ipt.place(x=100, y=50, width=550, height=30)
        return ipt

    def __tk_select_box_download(self, parent):
        cb = Combobox(
            parent,
            state="readonly",
        )
        cb["values"] = ("清华", "阿里", "豆瓣", "中科大", "百度")
        cb.place(x=590, y=0, width=60, height=30)
        return cb

    def __tk_check_button_downdload(self, parent):
        cb = Checkbutton(
            parent,
            text="指定镜像源",
        )
        cb.place(x=450, y=0, width=120, height=30)
        return cb

    def __tk_label_frame_lw1wx3j1(self, parent):
        frame = LabelFrame(
            parent,
            text="操作",
        )
        frame.place(x=0, y=110, width=670, height=100)
        return frame

    def __tk_button_download_start(self, parent):
        btn = Button(
            parent,
            text="开始下载",
            takefocus=False,
        )
        btn.place(x=100, y=20, width=80, height=30)
        return btn

    def __tk_button_open_path(self, parent):
        btn = Button(
            parent,
            text="打开路径",
            takefocus=False,
        )
        btn.place(x=300, y=20, width=80, height=30)
        return btn

    def __tk_button_download_infor(self, parent):
        btn = Button(
            parent,
            text="使用说明",
            takefocus=False,
        )
        btn.place(x=500, y=20, width=80, height=30)
        return btn

    def __tk_label_frame_lw1xjzul(self, parent):
        frame = LabelFrame(
            parent,
            text="输入",
        )
        frame.place(x=0, y=0, width=670, height=150)
        return frame

    def __tk_label_file_store(self, parent):
        label = Label(
            parent,
            text="库文件夹",
            anchor="center",
        )
        label.place(x=0, y=5, width=80, height=30)
        return label

    def __tk_label_target(self, parent):
        label = Label(
            parent,
            text="目标环境",
            anchor="center",
        )
        label.place(x=0, y=50, width=80, height=30)
        return label

    def __tk_label_target_file(self, parent):
        label = Label(
            parent,
            text="库名",
            anchor="center",
        )
        label.place(x=0, y=95, width=80, height=30)
        return label

    def __tk_input_file_store(self, parent):
        ipt = Entry(
            parent,
        )
        ipt.place(x=100, y=5, width=550, height=30)
        return ipt

    def __tk_input_target(self, parent):
        ipt = Entry(
            parent,
        )
        ipt.place(x=100, y=50, width=550, height=30)
        return ipt

    def __tk_input_target_file(self, parent):
        ipt = Entry(
            parent,
        )
        ipt.place(x=100, y=95, width=550, height=30)
        return ipt

    def __tk_label_frame_lw1xmj4y(self, parent):
        frame = LabelFrame(
            parent,
            text="操作",
        )
        frame.place(x=0, y=155, width=670, height=60)
        return frame

    def __tk_button_install_start(self, parent):
        btn = Button(
            parent,
            text="开始安装",
            takefocus=False,
        )
        btn.place(x=100, y=0, width=80, height=30)
        return btn

    def __tk_button_install_infor(self, parent):
        btn = Button(
            parent,
            text="使用说明",
            takefocus=False,
        )
        btn.place(x=480, y=0, width=80, height=30)
        return btn

    def __tk_button_install_uv(self, parent):
        btn = Button(
            parent,
            text="安装UV工具",
            takefocus=False,
        )
        btn.place(x=266, y=0, width=80, height=30)
        return btn

    def __tk_label_lw2524gb(self, parent):
        label = Label(
            parent,
            text="Python解释器",
            anchor="center",
        )
        label.place(x=0, y=250, width=80, height=30)
        return label

    def __tk_input_python_path(self, parent):
        ipt = Entry(
            parent,
        )
        ipt.place(x=100, y=250, width=550, height=30)
        return ipt

    def __tk_label_frame_log(self, parent):
        frame = LabelFrame(
            parent,
            text="工作日志",
        )
        frame.place(x=0, y=300, width=685, height=330)
        return frame

    def __tk_text_log(self, parent):
        text = Text(parent)
        text.place(x=0, y=0, width=675, height=300)
        return text


class Win(WinGUI):
    def __init__(self, controller):
        self.ctl = controller
        super().__init__()
        self.__event_bind()
        self.__style_config()
        self.ctl.init(self)

    def __event_bind(self):
        self.tk_tabs_menu.bind("<Button-1>", self.ctl.哈哈哈)
        pass

    def __style_config(self):
        pass


if __name__ == "__main__":
    win = WinGUI()
    win.mainloop()
