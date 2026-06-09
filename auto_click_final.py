"""
自动点击器 APP - 最终版

功能：用户输入坐标和间隔时间，自动点击指定位置
特点：100%免费，无广告
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
import threading
import time

try:
    from jnius import autoclass, cast
    from android import mActivity
    PLATFORM = 'android'
except ImportError:
    PLATFORM = 'desktop'


class AutoClickService:
    """自动点击服务"""
    
    def __init__(self):
        self.running = False
        self.thread = None
        
    def start(self, x, y, interval, count=-1):
        """开始自动点击"""
        self.running = True
        self.thread = threading.Thread(
            target=self._click_loop,
            args=(x, y, interval, count)
        )
        self.thread.daemon = True
        self.thread.start()
        
    def stop(self):
        """停止自动点击"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
            
    def _click_loop(self, x, y, interval, count):
        """点击循环"""
        clicked = 0
        
        if PLATFORM == 'android':
            # Android 平台
            try:
                View = autoclass('android.view.View')
                MotionEvent = autoclass('android.view.MotionEvent')
                activity = mActivity
                view = activity.getWindow().getDecorView()
                
                while self.running and (count == -1 or clicked < count):
                    down_time = long(time.time() * 1000)
                    event_time = long(time.time() * 1000)
                    
                    # ACTION_DOWN
                    motion_event = MotionEvent.obtain(
                        down_time, event_time,
                        MotionEvent.ACTION_DOWN,
                        float(x), float(y), 0
                    )
                    view.dispatchTouchEvent(motion_event)
                    motion_event.recycle()
                    
                    time.sleep(interval / 1000.0)
                    
                    # ACTION_UP
                    motion_event = MotionEvent.obtain(
                        down_time, event_time + int(interval),
                        MotionEvent.ACTION_UP,
                        float(x), float(y), 0
                    )
                    view.dispatchTouchEvent(motion_event)
                    motion_event.recycle()
                    
                    clicked += 1
                    
            except Exception as e:
                print(f"错误: {e}")
        else:
            # 桌面模式
            while self.running and (count == -1 or clicked < count):
                print(f"点击 ({x}, {y}) - 第 {clicked + 1} 次")
                time.sleep(interval / 1000.0)
                clicked += 1
                
    def is_running(self):
        return self.running


auto_click_service = AutoClickService()


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class AutoClickApp(App):
    title = '自动点击器'
    
    def build(self):
        sm = ScreenManager()
        
        # 主屏幕
        home = HomeScreen(name='home')
        self.setup_home_screen(home)
        sm.add_widget(home)
        
        # 设置屏幕
        settings = SettingsScreen(name='settings')
        self.setup_settings_screen(settings)
        sm.add_widget(settings)
        
        return sm
    
    def setup_home_screen(self, screen):
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # 标题
        layout.add_widget(Label(
            text='[b]自动点击器[/b]',
            font_size='24sp',
            size_hint_y=None,
            height=50,
            markup=True
        ))
        
        # 状态
        self.status_label = Label(
            text='状态: 未启动\n坐标: (0, 0)\n间隔: 0ms\n已点击: 0次',
            font_size='14sp',
            size_hint_y=None,
            height=120,
            halign='left',
            valign='top'
        )
        layout.add_widget(self.status_label)
        
        # 按钮
        btn_layout = GridLayout(cols=2, size_hint_y=None, height=100, spacing=10)
        
        self.start_btn = Button(
            text='[b]开始[/b]',
            background_color=(0.2, 0.8, 0.2, 1),
            markup=True
        )
        self.start_btn.bind(on_press=self.start_clicking)
        btn_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='[b]停止[/b]',
            background_color=(0.8, 0.2, 0.2, 1),
            disabled=True,
            markup=True
        )
        self.stop_btn.bind(on_press=self.stop_clicking)
        btn_layout.add_widget(self.stop_btn)
        
        layout.add_widget(btn_layout)
        
        # 设置按钮
        layout.add_widget(Button(
            text='[b]设置坐标[/b]',
            size_hint_y=None,
            height=50,
            background_color=(0.3, 0.5, 0.8, 1),
            markup=True,
            on_press=lambda x: self.go_to_settings()
        ))
        
        # 桌面提示
        if PLATFORM != 'android':
            layout.add_widget(Label(
                text='提示: 在 Android 上运行才能实际点击',
                font_size='12sp',
                color=(1, 0.5, 0, 1),
                size_hint_y=None,
                height=40
            ))
        
        screen.add_widget(layout)
    
    def setup_settings_screen(self, screen):
        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )
        
        # 返回
        layout.add_widget(Button(
            text='[b]返回[/b]',
            size_hint_y=None,
            height=40,
            background_color=(0.5, 0.5, 0.5, 1),
            markup=True,
            on_press=lambda x: self.go_to_home()
        ))
        
        # 标题
        layout.add_widget(Label(
            text='[b]点击设置[/b]',
            font_size='20sp',
            size_hint_y=None,
            height=40,
            markup=True
        ))
        
        # 表单
        form = GridLayout(
            cols=2,
            size_hint_y=None,
            height=200,
            spacing=10
        )
        
        form.add_widget(Label(text='X 坐标:'))
        self.x_input = TextInput(text='500', multiline=False, input_filter='int')
        form.add_widget(self.x_input)
        
        form.add_widget(Label(text='Y 坐标:'))
        self.y_input = TextInput(text='1000', multiline=False, input_filter='int')
        form.add_widget(self.y_input)
        
        form.add_widget(Label(text='间隔 (ms):'))
        self.interval_input = TextInput(text='1000', multiline=False, input_filter='int')
        form.add_widget(self.interval_input)
        
        form.add_widget(Label(text='点击次数:'))
        self.count_input = TextInput(text='-1', multiline=False, input_filter='int')
        form.add_widget(self.count_input)
        
        form.add_widget(Label(text='无限循环:'))
        self.infinite_checkbox = CheckBox(active=True)
        form.add_widget(self.infinite_checkbox)
        
        layout.add_widget(form)
        
        # 提示
        layout.add_widget(Label(
            text='提示: 开启开发者选项中的\n"指针位置"可查看坐标',
            font_size='12sp',
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=60
        ))
        
        # 保存按钮
        layout.add_widget(Button(
            text='[b]保存并返回[/b]',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.7, 0.3, 1),
            markup=True,
            on_press=self.save_settings
        ))
        
        screen.add_widget(layout)
    
    def go_to_settings(self):
        self.root.current = 'settings'
    
    def go_to_home(self):
        self.save_settings(None)
        self.root.current = 'home'
    
    def save_settings(self, instance):
        try:
            self.x = int(self.x_input.text) if self.x_input.text else 500
            self.y = int(self.y_input.text) if self.y_input.text else 1000
            self.interval = int(self.interval_input.text) if self.interval_input.text else 1000
            self.count = int(self.count_input.text) if self.count_input.text else -1
            if self.infinite_checkbox.active:
                self.count = -1
        except ValueError:
            self.x, self.y = 500, 1000
            self.interval, self.count = 1000, -1
        self.update_status()
    
    def update_status(self):
        if hasattr(self, 'status_label'):
            is_running = auto_click_service.is_running()
            status = "运行中" if is_running else "已停止"
            count_text = "无限" if self.count == -1 else str(self.count)
            self.status_label.text = (
                f'状态: {status}\n'
                f'坐标: ({self.x}, {self.y})\n'
                f'间隔: {self.interval}ms\n'
                f'目标: {count_text}'
            )
    
    def start_clicking(self, instance):
        self.save_settings(None)
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        auto_click_service.start(self.x, self.y, self.interval, self.count)
        self.update_status()
        Clock.schedule_interval(self.check_status, 0.5)
    
    def stop_clicking(self, instance):
        auto_click_service.stop()
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        Clock.unschedule(self.check_status)
        self.update_status()
    
    def check_status(self, dt):
        if not auto_click_service.is_running():
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            Clock.unschedule(self.check_status)
            self.update_status()
    
    def on_pause(self):
        return True


if __name__ == '__main__':
    AutoClickApp().run()
