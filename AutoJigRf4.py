import pyautogui
import keyboard
import time
import pygetwindow as gw

# --- 配置参数 ---
TARGET_WINDOW_TITLE = "Russian Fishing 4"  # 换成你目标程序的标题关键词
hold_time = 0.5  
gap_time = 2.0    

def is_target_active():
    """检查目标窗口是否处于最前端"""
    active_window = gw.getActiveWindow()
    if active_window is not None:
        # 判断目标关键词是否在当前窗口标题中
        return TARGET_WINDOW_TITLE.lower() in active_window.title.lower()
    return False

print(f"程序启动，目标窗口锁定为: {TARGET_WINDOW_TITLE}")
print("操作说明：[ 开始， ]停止")

try:
    while True:
        print(f"等待启动指令 [ ... (请确保目标窗口已打开)")
        keyboard.wait('[')
        
        active = True
        print("已进入监控状态...")
        
        while active:
            # 【核心逻辑】：只有目标窗口在最前面时，才执行操作
            if is_target_active():
                pyautogui.mouseDown(button='left')
                
                # 保持按住，期间检查停止键
                start_hold = time.time()
                while time.time() - start_hold < hold_time:
                    if keyboard.is_pressed(']'):
                        active = False
                        break
                    time.sleep(0.05)
                
                if not active: break
                pyautogui.mouseUp(button='left')
            else:
                # 如果当前不是目标窗口，程序会“静默等待”
                # 这里不打断循环，只是不操作鼠标，切回目标窗口后会自动恢复
                pass

            # 间隔时间等待，期间检查停止键
            start_gap = time.time()
            while time.time() - start_gap < gap_time:
                if keyboard.is_pressed(']'):
                    active = False
                    break
                time.sleep(0.05)
            
            if not active: break

        pyautogui.mouseUp(button='left')
        print("已停止循环，回到待命状态。\n")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n程序彻底退出。")