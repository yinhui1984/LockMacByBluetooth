#!/usr/bin/env python3

# 蓝牙设备名称
MY_BLE_DEVICE_NAME = "zhouyh-iPhone"
# 连续多少次检测到蓝牙设备不在附近后，锁定Mac
MAX_COUNT_IF_NOT_NEARBY = 5
# 信号强度低于多少就表示不表示不在附件
RSSI_THRESHOLD = -70

import asyncio
from bleak import BleakScanner
import time
import subprocess

async def get_nearby_ble_devices():
    scanner = BleakScanner()
    devices = await scanner.discover()
    device_list = [{"name": d.name, "address": str(d), "rssi": d.rssi} for d in devices]
    return device_list

def is_my_device_nearby():
    nearby_devices = asyncio.run(get_nearby_ble_devices())
    for device in nearby_devices:
        if device["name"] == MY_BLE_DEVICE_NAME:
            return True, device["rssi"]
    return False, None


def lock_mac():
    subprocess.run(["pmset", "displaysleepnow"])

# RSSI，Received Signal Strength Indicator（接收信号强度指示器），
# 是一个测量接收无线信号强度的指标，通常以分贝毫瓦（dBm）为单位表示。
# RSSI 是无线通信系统（例如 Wi-Fi 和蓝牙）中常用的一个参数，用于估计信号的质量和距离。

# 数值范围：
# RSSI 的值通常是负数，表示相对于 1 毫瓦的信号强度。较小（接近于零或正数）的 RSSI 值表示信号强度较强，而较大的负数值表示信号强度较弱。
# 信号强度：
# 通常，RSSI 值在 -30 dBm 到 -50 dBm 之间表示信号强度很强，可能是距离无线路由器或蓝牙设备很近。
# RSSI 值在 -50 dBm 到 -70 dBm 之间通常表示信号强度良好。
# RSSI 值在 -70 dBm 到 -90 dBm 之间可能表示信号强度较弱。
# RSSI 值低于 -90 dBm 通常表示信号非常弱，可能连接不稳定。


def lock_mac_if_need():
    not_near_by_count = 0
    while True:
        is_nearby, rssi = is_my_device_nearby()
        if is_nearby and rssi > -70:  # -70 dBm is an example threshold; adjust as needed
            not_near_by_count = 0
            print(f"My device is nearby with RSSI: {rssi}")
        else:
            not_near_by_count += 1
            print(f"My device is not nearby or weak signal, count: {not_near_by_count}, RSSI: {rssi}")

        if not_near_by_count >= MAX_COUNT_IF_NOT_NEARBY:
            print("My device is not nearby or weak signal for many times, lock the mac")
            not_near_by_count = 0
            lock_mac()
        time.sleep(2)


def main():
    try:
        lock_mac_if_need()
    except Exception as e:
        print(e) 

if __name__ == "__main__":
    main()






