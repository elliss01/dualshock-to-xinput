from pydualsense import *
import threading
import vgamepad as vg
import time
import argparse


ds = pydualsense()
try:
    ds.init()
except Exception as e:
    print("No device was found")
    print(e)
    time.sleep(5)

gamepad = vg.VX360Gamepad()

parser = argparse.ArgumentParser()
parser.add_argument("-r", help="Red Value of the led controller light", type=int, default=0)
parser.add_argument("-g", help="Green Value of the led controller light", type=int, default=0)
parser.add_argument("-b", help="Blue Value of the led controller light", type=int, default=255)
parser.add_argument("--brightness", help="sets the brightness of the controller light. 0-high, 1-medium, 2-low", type=int, choices=[0, 1, 2], default=0)
parser.add_argument("--noVibration", help="Disables vibration", action="store_false")
args = parser.parse_args()

shutdown_event = threading.Event()

ds.light.setColorI(args.r,args.g,args.b)
if args.brightness == 0:
    ds.light.setBrightness(Brightness.high)
elif args.brightness == 1:
    ds.light.setBrightness(Brightness.medium)
else:
    ds.light.setBrightness(Brightness.low)

triggermode = 1
ds.triggerL.setMode(TriggerModes.Off)
ds.triggerR.setMode(TriggerModes.Off)
ds.light.setPlayerID(PlayerID.PLAYER_1)

if args.noVibration:
    def vibration_handler(client, target, large_motor, small_motor, led_number, user_data):
        # print(f"Received notification for client {client}, target {target}")
        print(f"large motor: {large_motor}, small motor: {small_motor}")
        # print(f"led number: {led_number}")

        vibration_strength = 0

        if not large_motor + small_motor == 0:
            vibration_strength = round((large_motor + small_motor) / 2)
            ds.setLeftMotor(vibration_strength)
            ds.setRightMotor(vibration_strength)
        else:
            ds.setLeftMotor(0)
            ds.setRightMotor(0)

        # print(vibration_strength)

    gamepad.register_notification(callback_function=vibration_handler)

def mic_down(state):
    global triggermode

    if state:
        # print("mic button pressed")
        # print("switching mode")
        if triggermode == 2:
            triggermode = 1
        else:
            triggermode += 1

        if triggermode == 1:
            ds.triggerL.setMode(TriggerModes.Off)
            ds.triggerR.setMode(TriggerModes.Off)

            ds.light.setPlayerID(PlayerID.PLAYER_1)
            # print("setting 1")
        elif triggermode == 2:
            ds.triggerL.setMode(TriggerModes.Rigid)
            ds.triggerL.setForce(1, 255)
            ds.triggerR.setMode(TriggerModes.Rigid)
            ds.triggerR.setForce(1, 255)

            ds.light.setPlayerID(PlayerID.PLAYER_2)
            # print("setting 2")


ds.microphone_pressed += mic_down

def touch_down(state):
    if state:
        ds.light.setPlayerID(PlayerID.ALL)
    else:
        time.sleep(0.5)
        ds.light.setPlayerID(PlayerID.PLAYER_1)
        shutdown_event.set()

ds.touch_pressed += touch_down

def cross_down(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    gamepad.update()

def circle_down(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    gamepad.update()

def square_down(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    gamepad.update()

def triangle_down(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    gamepad.update()

ds.cross_pressed += cross_down
ds.circle_pressed += circle_down
ds.square_pressed += square_down
ds.triangle_pressed += triangle_down

def dpad_down_me(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    gamepad.update()

def dpad_up_me(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    gamepad.update()

def dpad_left_me(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    gamepad.update()

def dpad_right_me(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    gamepad.update()

ds.dpad_down += dpad_down_me
ds.dpad_up += dpad_up_me
ds.dpad_left += dpad_left_me
ds.dpad_right += dpad_right_me

def normalize(value):
    return max(-1.0, min(1.0, value / 128))


def update_joysticks():
    while not shutdown_event.is_set():
        lx = normalize(ds.state.LX)
        ly = -normalize(ds.state.LY)

        rx = normalize(ds.state.RX)
        ry = -normalize(ds.state.RY)

        gamepad.left_joystick_float(
            x_value_float=lx,
            y_value_float=ly
        )

        gamepad.right_joystick_float(
            x_value_float=rx,
            y_value_float=ry
        )

        gamepad.update()

        time.sleep(0.001) # 1000hz   0.001 1000hz  0.002 500  0.004 250

joystick_thread = threading.Thread(
    target=update_joysticks,
    daemon=True
)

joystick_thread.start()
print("started joystick thread")

# def left_joystick(stateX, stateY):
#     # print(f"stateX: {stateX}, stateY: {stateY}")
#     x = normalize(ds.state.LX)
#     y = -normalize(ds.state.LY)

#     gamepad.left_joystick_float(x_value_float=x, y_value_float=y)
#     gamepad.update()

# def right_joystick(stateX, stateY):
#     # print(f"stateX: {stateX}, stateY: {stateY}")
#     x = normalize(ds.state.RX)
#     y = -normalize(ds.state.RY)

#     gamepad.right_joystick_float(x_value_float=x, y_value_float=y)
#     gamepad.update()

# ds.left_joystick_changed += left_joystick
# ds.right_joystick_changed += right_joystick

def r1_change(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.update()

def l1_change(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    gamepad.update()

def r2_change(value):
    gamepad.right_trigger(value=value)
    gamepad.update()

def l2_change(value):
    gamepad.left_trigger(value=value)
    gamepad.update()

def r3_change(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_THUMB)
    gamepad.update()

def l3_change(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_THUMB)
    gamepad.update()

ds.r1_changed += r1_change
ds.l1_changed += l1_change
ds.r2_value_changed += r2_change
ds.l2_value_changed += l2_change
ds.r3_changed += r3_change
ds.l3_changed += l3_change

def share_down(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_BACK)
    gamepad.update()

def option_down(state):
    if state:
        gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    else:
        gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
    gamepad.update()

ds.share_pressed += share_down
ds.option_pressed += option_down

try:
    shutdown_event.wait()
finally:
    shutdown_event.set()
    joystick_thread.join()

    gamepad.reset()
    gamepad.update()

    ds.triggerL.setMode(TriggerModes.Off)
    ds.triggerR.setMode(TriggerModes.Off)
    ds.close()
    