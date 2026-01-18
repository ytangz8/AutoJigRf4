import pyautogui
import keyboard
import time
import pygetwindow as gw

# --- 配置参数 ---
TARGET_WINDOW_TITLE = "Russian Fishing 4" 
hold_time = 0.5  
gap_time = 2.0   

# 新增状态变量
is_manual_holding = False 

def is_target_active():
    """检查目标窗口是否处于最前端"""
    active_window = gw.getActiveWindow()
    if active_window is not None:
        return TARGET_WINDOW_TITLE.lower() in active_window.title.lower()
    return False

def toggle_manual_hold():
    """切换手动按住左键的状态"""
    global is_manual_holding
    if not is_target_active():
        return # 如果不是目标窗口，不触发

    if not is_manual_holding:
        pyautogui.mouseDown(button='left')
        is_manual_holding = True
        print(">>> 已开启持续收线 (按住左键)")
    else:
        pyautogui.mouseUp(button='left')
        is_manual_holding = False
        print(">>> 已停止持续收线 (松开左键)")

# 注册反斜杠快捷键（这种方式监听更灵敏，不阻塞主逻辑）
keyboard.add_hotkey('\\', toggle_manual_hold)

print(f"程序启动，目标窗口锁定为: {TARGET_WINDOW_TITLE}")
print("操作说明：")
print("  [ : 开始自动循环点按")
print("  ] : 停止自动循环点按")
print("  \\ : 开启/关闭持续收线 (手动长按模式)")

try:
    while True:
        print(f"等待启动指令 [ ... (或使用 \\ 键直接控制)")
        keyboard.wait('[')
        
        active = True
        print("已进入自动点按模式...")
        
        while active:
            # 如果此时开启了手动长按，则跳过自动循环逻辑，避免冲突
            if is_manual_holding:
                time.sleep(0.1)
                if keyboard.is_pressed(']'): active = False
                continue

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
            
            # 间隔时间等待
            start_gap = time.time()
            while time.time() - start_gap < gap_time:
                if keyboard.is_pressed(']'):
                    active = False
                    break
                # 在等待间隙如果切换了窗口，且处于长按状态，自动释放安全保护
                if is_manual_holding and not is_target_active():
                    pyautogui.mouseUp(button='left')
                    is_manual_holding = False
                    print("检测到窗口切换，已自动释放收线。")
                
                time.sleep(0.05)
            
            if not active: break

        pyautogui.mouseUp(button='left')
        is_manual_holding = False
        print("已停止自动循环，回到待命状态。\n")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\n程序彻底退出。")