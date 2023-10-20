#!/usr/bin/env python3

# 蓝牙设备名称
MY_BLE_DEVICE_NAME = "zhouyh-iPhone"
# 连续多少次检测到蓝牙设备不在附近后，锁定Mac
MAX_COUNT_IF_NOT_NEARBY = 5

import asyncio
from bleak import BleakScanner
import time
import subprocess

async def get_nearby_ble_devices():
    scanner = BleakScanner()
    devices = await scanner.discover()
    device_list = [{"name": d.name, "address": str(d)} for d in devices]
    return device_list

def is_my_device_nearby():
    nearby_devices = asyncio.run(get_nearby_ble_devices())
    for device in nearby_devices:
        if device["name"] == MY_BLE_DEVICE_NAME:
            return True
    return False


def lock_mac():
    subprocess.run(["pmset", "displaysleepnow"])



def lock_mac_if_need():
    not_near_by_count = 0
    while True:
        if is_my_device_nearby():
            not_near_by_count = 0
            print("My device is nearby")
        else:
            not_near_by_count += 1
            print("My device is not nearby, count: {}".format(not_near_by_count))

        if not_near_by_count >= MAX_COUNT_IF_NOT_NEARBY:
            print("My device is not nearby for many times, lock the mac")
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






