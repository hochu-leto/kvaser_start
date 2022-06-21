import time
from pprint import pprint
from canlib import canlib, connected_devices, Frame

'''
    canStatus = {
    canOK = 0,
    canERR_PARAM = -1,
    canERR_NOMSG = -2,
    canERR_NOTFOUND = -3,
      canERR_NOMEM = -4,
      canERR_NOCHANNELS = -5,
      canERR_INTERRUPTED = -6,
      canERR_TIMEOUT = -7,
      canERR_NOTINITIALIZED = -8,
      canERR_NOHANDLES = -9,
      canERR_INVHANDLE = -10,
      canERR_INIFILE = -11,
      canERR_DRIVER = -12,
      canERR_TXBUFOFL = -13,
      canERR_RESERVED_1 = -14,
      canERR_HARDWARE = -15,
      canERR_DYNALOAD = -16,
      canERR_DYNALIB = -17,
      canERR_DYNAINIT = -18,
      canERR_NOT_SUPPORTED = -19,
      canERR_RESERVED_5 = -20,
      canERR_RESERVED_6 = -21,
      canERR_RESERVED_2 = -22,
      canERR_DRIVERLOAD = -23,
      canERR_DRIVERFAILED = -24,
      canERR_NOCONFIGMGR = -25,
      canERR_NOCARD = -26,
      canERR_RESERVED_7 = -27,
      canERR_REGISTRY = -28,
      canERR_LICENSE = -29,
      canERR_INTERNAL = -30,
      canERR_NO_ACCESS = -31,
      canERR_NOT_IMPLEMENTED = -32,
      canERR_DEVICE_FILE = -33,
      canERR_HOST_FILE = -34,
      canERR_DISK = -35,
      canERR_CRC = -36,
      canERR_CONFIG = -37,
      canERR_MEMO_FAIL = -38,
      canERR_SCRIPT_FAIL = -39,
      canERR_SCRIPT_WRONG_VERSION = -40,
      canERR_SCRIPT_TXE_CONTAINER_VERSION = -41,
      canERR_SCRIPT_TXE_CONTAINER_FORMAT = -42,
      canERR_BUFFER_TOO_SMALL = -43,
      canERR_IO_WRONG_PIN_TYPE = -44,
      canERR_IO_NOT_CONFIRMED = -45,
      canERR_IO_CONFIG_CHANGED = -46,
      canERR_IO_PENDING = -47,
      canERR_IO_NO_VALID_CONFIG = -48,
      canERR__RESERVED = -49
    }
'''


def setUpChannel(channel=0,
                 openFlags=canlib.Open.ACCEPT_VIRTUAL,
                 outputControl=canlib.Driver.NORMAL):
    try:
        ch = canlib.openChannel(channel, bitrate=canlib.Bitrate.BITRATE_125K, flags=openFlags)
    except canlib.canError as ex:
        # pprint(dir(ex)) #.status)
        print(ex)
        return False

    ch.setBusOutputControl(outputControl)
    ch.busOn()
    return ch


def tearDownChannel(ch):
    ch.busOff()
    ch.close()


ch0 = setUpChannel(channel=0)
# pprint(dir(ch0))
# frame = Frame(
#     id_= 0x185017B8
#     data=[0x23, 0x40, 0x5B, 0x03, 0x18, 0xFC, 0xFF, 0xFF],
#     flags=canlib.MessageFlag.EXT
# )
# ch1.write(frame)

last_frame_time = int(round(time.time() * 1000))
last_received_frame = last_frame_time
period = 100
if ch0:
    frame = Frame(
        id_=0x185017B8,
        data=[0x23, 0x40, 0x5B, 0x01, 0x01, 0xFF, 0xFF, 0xFF],
        flags=canlib.MessageFlag.EXT
    )
    ch0.write(frame)
    frame_r = Frame(
        id_=0x185017B8,
        data=[0x23, 0x40, 0x5B, 0x04, 0x18, 0x03, 0xFF, 0xFF],
        flags=canlib.MessageFlag.EXT
    )

    while True:
        current_time = int(round(time.time() * 1000))
        try:
            if current_time > last_received_frame + period:
                last_received_frame = current_time
                ch0.write(frame_r)
            frame = ch0.read()
            print(hex(frame.id), end='    ')
            for i in frame.data:
                print(hex(i), end=' ')
            print()
            last_frame_time = int(round(time.time() * 1000))
        except canlib.canNoMsg:
            if current_time > last_frame_time + period:
                print('No CAN')
                tearDownChannel(ch0)
                break
        except canlib.canError as ex:
            print(ex)
            break
        except KeyboardInterrupt:
            frame = Frame(
                id_=0x185017B8,
                data=[0x23, 0x40, 0x5B, 0x01, 0x00, 0xFF, 0xFF, 0xFF],
                flags=canlib.MessageFlag.EXT
            )
            ch0.write(frame)
            print("Stop.")
            break
else:
    for dev in connected_devices():
        print(dev.probe_info())
