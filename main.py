import time
from alpaca.telescope import *  # Multiple Classes including Enumerations
from alpaca.exceptions import *  # Or just the exceptions you want to catch

import constant
from constant import *

#继承于ASCOM.Equipment.Telescope的子类
class myTelescope(Telescope):
    def __init__(self, address, device_number):
        super().__init__(address, device_number)

    def moving_axis(self, axis_num: int, rate: float,isFineAdjustment:bool):
        sleep_time = 3

        if axis_num not in [0, 1]:
            raise ValueError("Axis range must from 0 to 2!")
        else:
            axis = constant.move_axis[axis_num]
            rate_range = self.AxisRates(axis)[0] if isFineAdjustment else self.AxisRates(axis)[1]
            #这里有一个ASCOM协议自己限定的赤道仪转速范围，存在constant.py中
            if abs(rate)<rate_range.minv or abs(rate)>rate_range.maxv:
                raise ValueError("Moving rate of telescope must be in given range!")
            try:
                self.MoveAxis(axis, rate)
                time.sleep(sleep_time)
                print("Telescope successfully moved in axis " + str(axis_num) + " with rate " + str(rate)+ " degree per second")
                self.MoveAxis(axis, 0)


            except Exception as e:
                print(f'Moving failed: {str(e)}')


if __name__ == '__main__':
    T = myTelescope('localhost:32323', 0)
    print(T.EquatorialSystem)
    print(T.api_version)  # Local Omni Simulator
    try:
        T.Connected = False
        T.Connected = True
        print(f'Connected to {T.Name}')
        print(T.Description)
        T.Tracking = False # Needed for slewing (see below)
        T.FindHome()
        print('Starting moving...')
        T.moving_axis(0, 6, isFineAdjustment=True)
        T.moving_axis(0, -1, isFineAdjustment=True)

    except Exception as e:
        print(f'Slew failed: {str(e)}')
    finally:  # Assure that you disconnect
        print("Disconnecting...")
    #程序末尾要记得断开与设备的连接，否则可能会影响后续使用
        T.Connected = False
