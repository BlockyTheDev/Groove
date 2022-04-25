<p align="center">
  <img width="12%" align="center" src="../app/resource/images/logo/logo.png" alt="logo">
</p>
  <h1 align="center">
  Groove 音乐
</h1>
<p align="center">
  一个基于 PyQt5 和 LAV Filters 的音乐播放器.
</p>

<p align="center">

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.8.6-blue.svg?color=00B16A" alt="Python 3.8.6"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyQt-5.15.2-blue?color=00B16A" alt="PyQt 5.15.2"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/LAV%20Filters-0.74.1-blue?color=00B16A" alt="LAV Filters 0.74.1"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/OS-Win%2010%20|%20Win%2011-blue?color=00B16A" alt="OS Win10 | Win11"/>
  </a>
</p>

<p align="center">
<a href="../README.md">English</a> | 简体中文
</p>

## 界面
![界面](./screenshot/Groove音乐.png)

## 功能

* 播放本地音乐

  ![local music](screenshot/本地音乐.gif)

* 搜索、播放和下载在线音乐

  ![online music](screenshot/在线音乐.gif)

* 创建和管理个人播放列表

  ![custom playlist](screenshot/播放列表.gif)

* 查看和编辑歌曲元数据

  ![song meta data](screenshot/歌曲信息.gif)

* 观看和下载在线 MV

  ![MV](screenshot/播放和下载MV.png)


## 快速开始
1. 创建虚拟环境:

    ```shell
    conda create -n Groove python=3.8
    conda activate Groove
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
    ```

2. 下载并安装 [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases/download/0.74/LAVFilters-0.74-Installer.exe).
3. 打开 Groove 音乐:

    ```shell
    cd app
    conda activate Groove
    python Groove.py
    ```

## 安装
1. 下载并安装 [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases/download/0.74/LAVFilters-0.74-Installer.exe).
2. 从 [Release](https://github.com/zhiyiYo/Groove/releases) 页面下载 `Groove_v*.*.*_windows_x64.zip`.
3. 解压 `Groove_v*.*.*_windows_x64.zip`
4. 在解压出来的 `Groove` 文件夹中，找到并双击运行 **Groove.exe**
5. 开启你的音乐之旅 😊~~



## 常见问题
* **为什么窗口拖动的时候会出现卡顿现象？**

  由于界面使用了亚克力窗口特效，在某些版本的 Win10 上会出现这个问题。有三种解决方案:

  * 更新 Win10 到最新版本，比如 Win11.
  * 取消复选框的选中 **高级系统设置 --> 性能 --> 拖动时显示窗口内容**.
  * 在设置界面禁用亚克力效果.

* **支持哪些格式的音频文件呀？**

  目前支持以下几种的音频文件:
  * mp3
  * flac
  * mp4/m4a


## 许可证
```txt
MIT License

Copyright (c) 2022 Zhengzhi Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```