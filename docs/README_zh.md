<p align="center">
  <img width="15%" align="center" src="../app/resource/images/logo/logo.png" alt="logo">
</p>
  <h1 align="center">
  Groove 音乐
</h1>
<p align="center">
  一个基于 PyQt5 的跨平台音乐播放器
</p>

<p align="center">

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Python-3.8.6-blue.svg?color=00B16A" alt="Python 3.8.6"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyQt-5.15.2-blue?color=00B16A" alt="PyQt 5.15.2"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=00B16A" alt="Platform Win32 | Linux | macOS"/>
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

2. 下载解码器：
   * 对于 Win32，安装 [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases/download/0.74/LAVFilters-0.74-Installer.exe)
   * 对于 Linux，安装 GStreamer


3. 打开 Groove 音乐:

    ```shell
    cd app
    conda activate Groove
    python Groove.py
    ```

## 安装
### Win32
#### 安装包
1. 下载并安装 [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases/download/0.74/LAVFilters-0.74-Installer.exe)
2. 从 [Release](https://github.com/zhiyiYo/Groove/releases) 页面下载 `Groove_v*.*.*_x64_setup.exe`
3. 右键并以管理员身份运行 `Groove_v*.*.*_x64_setup.exe`，根据安装向导完成 Groove 的安装
4. 开启你的音乐之旅 😊~~

#### 免安装版
1. 下载并安装 [LAV Filters](https://github.com/Nevcairiel/LAVFilters/releases/download/0.74/LAVFilters-0.74-Installer.exe)
2. 从 [Release](https://github.com/zhiyiYo/Groove/releases) 页面下载 `Groove_v*.*.*_windows_x64.zip`
3. 解压 `Groove_v*.*.*_windows_x64.zip`
4. 在解压出来的 `Groove` 文件夹中，找到并双击运行 **Groove.exe**
5. 开启你的音乐之旅 😊~~

### Linux
1. 安装 GStreamer
2. 从 [Release](https://github.com/zhiyiYo/Groove/releases) 页面下载 `Groove_v*.*.*_linux_x64.zip`
3. 解压 `Groove_v*.*.*_linux_x64.zip`
4. 在解压出来的 `Groove` 文件夹中，找到并双击运行 **Groove** 可执行文件
5. 开启你的音乐之旅 😊~~


## 常见问题
* **为什么窗口拖动的时候会出现卡顿现象？**

  由于界面使用了亚克力窗口特效，在某些版本的 Win10 上会出现这个问题。有三种解决方案:

  * 更新 Win10 到最新版本，比如 Win11.
  * 取消复选框的选中 **高级系统设置 --> 性能 --> 拖动时显示窗口内容**.
  * 在设置界面禁用亚克力效果.

* **支持哪些格式的音频文件呀？**

  目前支持下述格式的音频文件:
  * True Audio File(*.tta)
  * WAVE Audio File(*.wav)
  * WavPack Audio File(*.wv)
  * Audio Codec 3 File(*.ac3)
  * Ogg Opus Audio File(*.opus)
  * Ogg Vorbis Audio File(*.ogg)
  * MPEG File(*.mp3, *.m4a, *.mp4)
  * Windows Media Audio File(*.wma)
  * Advanced Audio Coding File(*.aac)
  * Advanced Systems Format File(*.asf)
  * Audio Interchange File Format(*.aiff)
  * Free Lossless Audio Codec File(*.flac)
  * Musepack Compressed Audio File(*.mpc)
  * Monkey's Audio Lossless Audio File(*.ape)

* **为什么运行的时候 GStreamer 报错：Warning: "No decoder available for type ..."?**

  可以尝试 `sudo apt-get install gstreamer1.0-libav` 来解决该问题，Ubuntu 20.04 亲测有效。

* **支持哪些格式的歌词文件呀？**

  目前支持 `.lrc` 和 `.json` 格式的歌词文件，更多信息请参见 [歌词文件格式说明](./lyrics_format.md)。
