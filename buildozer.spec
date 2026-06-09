# Buildozer 配置文件
# 用于将 Python Kivy 程序打包成 Android APK

[app]

# 应用标题
title = AutoClicker

# 应用包名（必须是唯一的域名格式）
package.name = autoclicker

# 应用域名
package.domain = com.example

# 应用版本
version = 1.0

# 应用源码
source.include_exts = py,png,jpg,kv,atlas

# 主程序入口
source.target_arch = armeabi-v7a,arm64-v8a,x86,x86_64

# Kivy 版本（使用默认）
# requirements = kivy

# 屏幕方向
orientation = portrait

# 全屏模式
fullscreen = 0

# Android 权限
android.permissions = WRITE_SETTINGS

# Android API 最低版本
android.minapi = 21

# Android API 目标版本
android.api = 29

# 是否显示状态栏
android.statusbar.visible = True

# 是否保持屏幕常亮
android.keepscreen = True

# 窗口配置（Kivy 1.x 使用）
[window]

# 窗口大小（仅桌面有效）
# width = 360
# height = 600

# 标题
# title = 自动点击器

[kivy]

# 日志级别
log_level = info

# 是否显示FPS
# show_fps = True

# 默认字体
# fontname = Roboto

[buildozer]

# 日志文件
log_file = buildozer.log

# 是否显示构建输出
show_build_output = True

# 构建模式
build_mode = release
