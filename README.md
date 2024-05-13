# 程序说明
python工具，使用tkinter实现gui设计，用于在线下载第三方库wheel文件，离线安装第三方库wheel文件。适合需要从外网导入第三方库进内网的朋友，本工具提供了在线下载和离线安装两个功能模块。
#在线下载
本模块基于pip download命令实现下载指定的第三方库，指定的requirement.txt所包含的库，实现将tar.gz文件构建位whl文件。使用前会自动读取系统python解释器位置，以此调用pip命令，可以自己指定python解释器，来实现指定python版本的第三方库下载。
#离线安装
本模块基于uv pip install命令实现安装指定的第三方库，指定的requirement.txt所包含的库，若指定的项目地址不存在虚拟环境，则使用uv v 命令创建。
tips：win7下，不支持uv 0.1.39以上版本。

#项目依赖
本项目基于python标准库实现，不包含第三方依赖。

