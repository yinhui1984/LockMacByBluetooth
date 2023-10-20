# LockMacByBluetooth
 小工具，指定的蓝牙设备不在电脑旁边时则锁定Mac

## how to use
1. 修改 `MY_BLE_DEVICE_NAME = "zhouyh-iPhone"` 为你自己是蓝牙设备名称, 运行main.py即可
2. 如果想做成服务，则 `make` 生成plist文件，然后`make install`进行安装，卸载则使用`make uninstall`

## 原理很简单
扫描周围的蓝牙设备，连续几次没找到指定设备或信号强度低于一定值则锁定.
锁定时使用的是 `pmset displaysleepnow` 因为它不需要任何特殊的系统权限，所以实际是息屏，但在系统设置中的“显示器关闭后需要密码”设置为“立即”就达到了锁定效果

我试了自己的iphone，不必在意手机蓝牙是否开启，只要在附近就可以了。关闭蓝牙后同样可以扫描到。只有关机才不会被扫描到。