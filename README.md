# AutoClicker

无广告的 Android 自动点击器 APP

## 功能

- 输入 X, Y 坐标
- 设置点击间隔（毫秒）
- 设置点击次数（支持无限循环）
- 一键开始/停止
- 100% 免费，无广告

## 下载

APK 下载地址：https://github.com/YOUR_USERNAME/auto-clicker/releases

## 源码运行（需要 Termux）

```bash
pkg update && pkg install python
pip install kivy
python auto_click_final.py
```

## 打包 APK

使用 GitHub Actions 自动打包，推送代码后即可下载 APK。

## 获取坐标

在手机上开启 **开发者选项** → **指针位置**，即可看到触摸坐标。
