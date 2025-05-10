"""工具main模块定义"""

import os
import re
import shutil
import subprocess
import sys
import tarfile
import threading
from pathlib import Path
from queue import Queue
from tkinter import ACTIVE, DISABLED, BooleanVar, filedialog, messagebox
from gui import WinGUI


class ReStd(Queue):
    """继承Queue，实现重定向数据传输"""

    def __init__(self):
        Queue.__init__(self)

    def write(self, content):
        """将消息放入队列"""
        self.put(content)

    def flush(self):
        """定义flush"""
        return


def execute_command(command: str, cwd: Path = None) -> tuple:
    """使用subprocess执行下载命令，并捕获输出"""
    try:
        output_lines = []
        with subprocess.Popen(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=True,
        ) as process:
            for line in process.stdout:
                # 立即打印每一行输出，flush=True确保内容立即输出而不等待缓冲区满
                print(line, end="", flush=True)
                output_lines.append(line)  # 将每行添加到列表中
            captured_output = "".join(output_lines)
        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        return process, captured_output, process.returncode

    except FileNotFoundError:
        print(f"无法找到命令：{command.split()[0]}")
        return None, "命令未找到", -1

    except Exception as e:
        print(f"执行命令时发生错误：{str(e)}，可能不存在对应安装包")
        return None, f"执行错误：{str(e)}", -2


class DownLoad(WinGUI):
    """用于下载页功能实现类"""

    def __init__(self):
        super().__init__()
        self.v2 = BooleanVar()
        self.python_path = None
        self.download_path = ""
        self.target_package = None
        self.init_components()
        self.download_link = {
            "清华": "https://pypi.tuna.tsinghua.edu.cn/simple/",
            "阿里": "https://mirrors.aliyun.com/pypi/simple/",
            "豆瓣": "https://pypi.douban.com/simple/",
            "中科大": "https://pypi.mirrors.ustc.edu.cn/simple/",
            "百度": "https://mirror.baidu.com/pypi/simple",
        }

    def init_components(self):
        """初始化界面"""
        self.configure_gui()
        self.bind_events()

    def configure_gui(self):
        """初始化界面参数"""
        self.tk_check_button_downdload.config(variable=self.v2)
        self.tk_input_path.config(state="readonly")
        self.tk_select_box_download.current(0)
        if "runtime" in sys.exec_prefix:  # 区别打包环境
            icon_file = Path.cwd().joinpath("runtime\\down.ico")
        else:
            icon_file = Path.cwd().joinpath("down.ico")
        self.wm_iconbitmap(str(icon_file))
        self.get_python_path()

    def get_python_path(self):
        """获取python路径"""
        command = ["where", "python"]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )
        if result.returncode != 0:
            print("找不到python,请设置！")
        else:
            python_path = str(result.stdout).split("\n", maxsplit=1)[0]
            if Path(python_path).exists() and Path(python_path).suffix == ".exe":
                self.tk_input_python_path.delete(0, "end")
                self.tk_input_python_path.insert(0, python_path)

    def bind_events(self):
        """绑定点击事件"""
        self.tk_button_download_start.config(command=self.start_download)
        self.tk_button_save_path.config(command=self.save_path)
        self.tk_button_open_path.config(command=self.open_path)
        self.tk_button_download_infor.config(command=self.show_system_info)

    @staticmethod
    def show_system_info() -> None:
        """下载页使用说明"""
        message = (
            "本页用于下载第三方库文件，包括指定库及其依赖，自动构建wheel文件"
            "并将下载的文件存放于指定目录。\n要求系统已安装Python环境。\n\n"
            "实现原理：利用pip download功能下载第三方库。\n\n"
            "首先给出python解释器的路径，用它来调用pip工具，以此确定第三方库python版本\n"
            "使用示例：\n"
            "第三方库名：pandas\n"
            "第三方库名：-r path-to-requirements.txt\n"
            "第三方库名：-r path-to-requirements.txt 跟一切' pip download '中的可用命令\n"
        )
        messagebox.showinfo(title="程序说明", message=message)

    def save_path(self) -> None:
        """设置库文件保存位置"""
        self.download_path = filedialog.askdirectory()
        self.tk_input_path.config(state="normal")
        self.tk_input_path.delete(0, "end")
        self.tk_input_path.insert(0, self.download_path or "")
        self.tk_input_path.config(state="readonly")

    def open_path(self) -> None:
        """打开文件夹"""
        if self.download_path:
            os.startfile(self.download_path)

    def start_download(self) -> None:
        """开始下载"""
        self.python_path = self.tk_input_python_path.get()
        if not self.python_path:
            messagebox.showinfo(title="提示", message="请设置python解释器路径")
            return
        self.target_package = self.tk_input_package.get().strip()
        if not self.download_path or not self.target_package:
            messagebox.showerror("错误", "请输入正确的第三方库名与保存路径！")
            return
        self.tk_text_log.delete(1.0, "end")
        down_thread = threading.Thread(target=self.download_thread_func, daemon=True)
        down_thread.start()
        # with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        #     future = executor.submit(self.download_thread_func)
        self.tk_button_download_start.config(state=DISABLED)

    def download_thread_func(self) -> None:
        """下载线程，函数实现"""
        command = self.construct_pip_command()
        _, stdout, return_code = execute_command(command)
        if return_code == 0:
            print("完成下载".center(80, "*"))
            self.extract_downloaded_files(stdout)
            folder_path = Path(self.download_path).joinpath("out")
            if folder_path.exists():
                try:
                    shutil.rmtree(folder_path)
                    print(f"文件夹 '{folder_path}' 及其内容已被成功删除。")
                except OSError as e:
                    print(f"删除文件夹时发生错误: {e.strerror}")
            messagebox.showinfo(title="成功", message="已完成所有下载！")

        else:
            print("下载失败\n")
        self.tk_button_download_start.config(state=ACTIVE)

    def construct_pip_command(self) -> str:
        """构建下载命令"""
        pip_command = [
            f'"{self.python_path}"',
            "-m",
            "pip",
            "download",
            "-d",
            f'"{self.download_path}"',
            self.target_package,
        ]
        if self.v2.get():
            mirror = self.download_link[self.tk_select_box_download.get()]
            pip_command.extend(["-i", mirror])
        return " ".join(pip_command)

    def extract_downloaded_files(self, output: str) -> None:
        """释放下载的文件"""
        pattern = r"(?<=Saved)(.*)(?=Successfully)"  # 正则表达式模式
        matches = re.findall(
            pattern, output, re.DOTALL
        )  # 使用re.DOTALL使.匹配包括换行符在内的任意字符
        extracted_text = matches[0].strip() if matches else None
        file_names = []
        if extracted_text:
            file_names = extracted_text.replace("Saved ", "").split("\n")
            file_names = [
                Path(self.download_path).joinpath(Path(file).name)
                for file in file_names
            ]
        if "already downloaded" in output:
            pattern = r"File was already downloaded\s+(.*?\.(?:tar\.gz|whl))"

            # 使用findall方法找到所有匹配项
            file_paths = re.findall(pattern, output)

            file_names.extend(file_paths)
        file_names = [
            Path(self.download_path).joinpath(Path(file).name) for file in file_names
        ]
        self.make_wheels(file_names)

    def make_wheels(self, whl_names: list[Path]) -> None:
        """将.tar.gz文件编译为wheel"""
        tars = self.check_tar_gz(whl_names)
        if tars:
            print(f"发现tar.gz压缩包，合计{len(tars)}个,开始自动构建wheel文件")
            total_count = len(tars)
            for idx, tar in enumerate(tars):
                self.build_wheel(tar, self.download_path)
                print(f"剩余{total_count - 1 - idx}个还未构建".center(80, "*"))

    @staticmethod
    def check_tar_gz(file_list: list[Path]) -> list[Path]:
        """检查是否存在.tar.gz文件，该文件需在线编译"""
        tars = []
        for file_name in file_list:
            if file_name.suffix == ".gz":
                tars.append(file_name)
        return tars

    def build_wheel(self, tar: Path, download_path: str) -> None:
        """使用pip wheel . 命令构建wheel文件"""
        with tarfile.open(tar, "r:gz") as tar_sub:
            tar_sub.extractall(path=Path(download_path).joinpath("out"))
        command = [f"{self.python_path}", "-m", "pip", "wheel", "."]

        dir_name = str(tar.stem).replace(".tar", "")
        current_path = str(Path().cwd())
        cwd = Path(download_path).joinpath(f"out\\{dir_name}")
        command_str = " ".join(command)
        result, stdout, return_code = execute_command(command_str, cwd=cwd)
        if return_code != 0:
            print(f"wheel文件构建失败:\n{result.stderr}")
            os.chdir(current_path)
            return
        print(f"{tar.stem}：wheel文件构建成功".center(80, "*"))

        self.get_wheel_name(
            stdout,
            download_path,
            Path(download_path).joinpath(f"out\\{dir_name}"),
        )
        os.chdir(current_path)

    def get_wheel_name(self, message: str, download_path: str, file_path: Path) -> None:
        """获取编译生成的wheel文件名"""
        pattern = r"filename=(.+\.whl)"
        match = re.search(pattern, message)
        try:
            filename = match.group(1)
            file_path = file_path.joinpath(filename)
            self.move_wheel_file(file_path, Path(download_path).joinpath(filename))
        except AttributeError:
            pass

    @staticmethod
    def move_wheel_file(filename: Path, new_path: Path) -> None:
        """将生成的wheel文件移动到设置的库下载文件夹"""
        try:
            filename.rename(new_path)
        except FileExistsError:
            pass


class Install(WinGUI):
    """库安装类定义"""

    def __init__(self):
        super().__init__()
        self.uv = None
        self.ini_window()

    def ini_window(self):
        """初始化界面"""
        self.tk_button_install_start.config(command=self.start)
        self.tk_button_install_infor.config(command=self.install_infor)
        self.tk_button_install_uv.config(command=self.install_uv)
        self.tk_input_file_store.delete(0, "end")
        self.tk_input_file_store.insert(0, "E:\\导入\\第三方库导入")
        self.tk_input_target.delete(0, "end")
        self.tk_input_target.insert(0, r"D:\python\fastui")
        self.tk_input_target_file.delete(0, "end")
        self.tk_input_target_file.insert(0, "matplotlib")
        self.uv = self.check_uv()

    @staticmethod
    def check_uv() -> bool:
        """用于检测是否安装了UV"""
        command_str = "uv -V"
        _, _, return_code = execute_command(command_str)
        if return_code != 0:
            messagebox.showwarning(
                title="警告", message="UV工具不存在，无法使用离线安装功能"
            )
            return False
        return True

    def install_uv(self):
        python_path = self.tk_input_python_path.get()
        if not python_path:
            messagebox.showerror(
                title="指定python路径",
                message="请将python解释器绝对路径复制粘贴到python解释器输入框中",
            )
            return
        uv_file = Path.cwd().joinpath(
            "runtime/uv-0.1.39-py3-none-win_amd64.whl"
        )  # 该版本支持win7
        command = [
            f'"{python_path}"',
            "-m",
            "pip",
            "install",
            f'"{uv_file}"',
            "--no-cache-dir",
            "--no-index",
        ]
        command_str = " ".join(command)
        print(command_str)
        _, _, return_code = execute_command(command_str)
        if return_code != 0:
            print("uv工具安装失败\n")
            self.tk_button_install_start.config(state=ACTIVE)
            return
        print("uv工具安装成功")

    def start(self) -> None:
        """开始安装第三方库"""
        if self.uv:
            install_thread = threading.Thread(target=self.thread_func, daemon=True)
            self.tk_button_install_start.config(state=DISABLED)
            install_thread.start()
        else:
            print(
                "虚拟环境创建失败，请使用' pip install uv '或"
                "' pip install uv --no-index -f path-to-uv-wheel ' 安装UV工具\n"
                "或点击 安装UV工具 按钮进行安装"
            )
            return

    # pip install uv --no-cache-dir --no-index -f E:\导入\测试
    def thread_func(self) -> None:
        """线程，安装第三方库"""
        target_path = self.tk_input_target.get()
        target_file = self.tk_input_target_file.get()
        if "-r" in target_file:
            target_file = target_file.split(" ")
        else:
            target_file = [target_file]
        file_store = self.tk_input_file_store.get()
        # 判断项目下是否存在venv环境
        venv_path = Path(target_path).joinpath(".venv\\Scripts\\activate.bat")
        cwd = Path(target_path)
        if not venv_path.exists():
            command = ["uv", "venv", f'--python="{self.tk_input_python_path.get()}"']
            command_str = " ".join(command)

            _, _, return_code = execute_command(command_str, cwd=cwd)
            if return_code != 0:
                print("虚拟环境创建失败，请使用' pip install uv ' 安装UV工具\n")
                self.tk_button_install_start.config(state=ACTIVE)
                return
            print("虚拟环境创建成功")
        self.tk_button_install_start.config(state=ACTIVE)
        de_venv_path = venv_path.parent.joinpath("deactivate.bat")
        commands = [
            [str(venv_path)],
            ["uv", "pip", "install", "--offline", f'-f="{file_store}"', *target_file],
            [str(de_venv_path)],
        ]
        for command in commands:
            command_str = " ".join(command)
            _, _, return_code = execute_command(command_str, cwd=cwd)
            if return_code != 0:
                print(f"第三方库安装失败:\n{return_code}")
                self.tk_button_install_start.config(state=ACTIVE)
                return
        print("第三方库安装成功！".center(80, "*"))
        messagebox.showinfo(title="安装完成", message="第三方库安装成功!")

    @staticmethod
    def install_infor() -> None:
        """安装页使用说明"""
        message = (
            "实现原理：利用' uv pip install --offline -f=path-to-wheel '来实现离线快速安装。"
            "若指定的文件夹虚拟环境不存在，会自动使用' uv v '命令创建虚拟环境\n\n"
            "库文件夹：第三方库wheel文件所在文件夹；\n"
            "目标环境：第三方库安装位置，若该处不存在虚拟环境，将使用'uv v'命令创建虚拟环境；\n"
            "库名：需要安装的第三方库名字，如matplotlib。\n"
            "使用示例\n"
            "库名：matplotlib\n"
            "库名：-r path-to-requirements.txt\n"
            "库名：-r path-to-requirements.txt 跟一切'uv pip install '中的可用命令\n"
        )
        messagebox.showinfo(title="使用说明", message=message)


class MainWindow(DownLoad, Install):
    """继承两个功能页"""

    def __init__(self):
        super().__init__()
        self.queue = ReStd()  # 重定向输出
        self.tk_tabs_menu.bind("<<NotebookTabChanged>>", self.change_menu)
        self.__init_gui()

    def __init_gui(self) -> None:
        """重定向输出，并进入show_msg循环"""
        sys.stdout = self.queue
        self.after(100, self.show_msg)

    def show_msg(self):
        """使用after方法更新主界面"""
        while not self.queue.empty():
            content = self.queue.get()
            self.tk_text_log.insert("end", content)
            self.tk_text_log.see("end")
        self.after(100, self.show_msg)

    def change_menu(self, _) -> None:
        """设置切换事件，若第三方库,库目录已设置，则自动复制到安装页"""
        download_path = self.tk_input_path.get()
        target_package = self.tk_input_package.get()
        if self.tk_tabs_menu.index(self.tk_tabs_menu.select()) and download_path:
            self.tk_input_file_store.delete(0, "end")
            self.tk_input_file_store.insert(0, download_path)
        if self.tk_tabs_menu.index(self.tk_tabs_menu.select()) and target_package:
            self.tk_input_target_file.delete(0, "end")
            self.tk_input_target_file.insert(0, target_package)


if __name__ == "__main__":
    window = MainWindow()
    window.mainloop()

#nuitka --windows-icon-from-ico=down.ico main.py
