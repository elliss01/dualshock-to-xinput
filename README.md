> **Non-commercial software**
>
> Free to use, modify, fork, and share. Commercial use and selling the
> software are not permitted. See the [LICENSE](LICENSE) for details.

# DualSense to XInput

A simple Python program that translates PlayStation DualSense controller
inputs into a virtual Xbox 360 controller using PyDualSense and vgamepad.

This allows a DualSense controller to be used with games that only support
XInput/Xbox controllers.

## Features

- DualSense controller input
- Virtual Xbox 360 controller output
- Analog sticks
- Triggers
- Buttons
- D-pad

## Requirements

- Windows 10/11
- Python 3.x
- PlayStation DualSense controller
- ViGEmBus driver (should install with the python module)

## Installation

```powershell
pip install -r requirements.txt
python main.py
```

## Controls

| DualSense input       | Function                                                  |
| --------------------- | --------------------------------------------------------- |
| **Click Touchpad**    | Stops the program                                         |
| **Microphone Button** | Switches trigger preset between **Default** and **Rigid** |

The **PS button** is currently not mapped. This is intentional, as it isn't required for the controller to function as an Xbox 360 controller. Depending on the game and Windows configuration, the PS button may still have its normal system/Steam behavior.

## Command-Line Usage

The program supports several command-line options for configuring the controller.

### Controller Light

```text
-r <0-255>        Red value
-g <0-255>        Green value
-b <0-255>        Blue value
```

Each value can be between **0 and 255**.

The blue value defaults to `255`, so if you want to completely disable blue, you must explicitly specify:

```text
-b 0
```

For example:

```powershell
.\PS5Controller -r 255 -b 0
```

sets the controller light to **red**.

Setting all three values to `0` turns the controller light off:

```powershell
.\PS5Controller -r 0 -g 0 -b 0
```

### Player Icon Brightness

```text
--brightness <0-2>
```

Controls the brightness of the player indicator icons.

| Value | Brightness     |
| ----: | -------------- |
|   `0` | High (default) |
|   `1` | Medium         |
|   `2` | Low            |

### Vibration

```text
--noVibration
```

Disables controller vibration.

## Examples

### Red light with vibration disabled

```powershell
.\PS5Controller -r 255 -b 0 --noVibration
```

Sets the controller light to red and disables vibration.

### White light, medium player icon brightness, no vibration

```powershell
.\PS5Controller -r 255 -g 255 -b 255 --brightness 1 --noVibration
```

Sets the controller light to white, the player indicator brightness to medium, and disables vibration.

### Purple light

```powershell
.\PS5Controller -r 255 -b 255
```

Sets the controller light to purple.

## Known Issue

While testing, I found that **restarting the program while a game is already running can cause controller vibration to stop working**.

If this happens, restarting the game should restore vibration functionality.

## Notes

The program creates a virtual Xbox 360 controller, allowing the DualSense to be used with games that support XInput controllers.

The program is designed primarily for Windows and requires the appropriate virtual gamepad driver to be installed.


## License

This project is licensed under the **PolyForm Noncommercial License 1.0.0**.

You are free to:

* Use the software for personal and non-commercial purposes
* Modify the source code
* Fork the project on GitHub
* Create and share modified versions
* Include the software in other free, non-commercial projects

You may **not**:

* Sell this software
* Sell modified versions of this software
* Create a paid version of this software
* Use this software for commercial purposes

See the [`LICENSE`](LICENSE) file for the complete license terms.

**Copyright © 2026 Ellis Godwin**
