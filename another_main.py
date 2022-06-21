from canlib import canlib, Frame


def setUpChannel(channel=0,
                 openFlags=canlib.Open.ACCEPT_VIRTUAL,
                 outputControl=canlib.Driver.NORMAL):
    try:
        ch = canlib.openChannel(channel, bitrate=canlib.Bitrate.BITRATE_125K, flags=openFlags)
    except canlib.canError as ex:
        print(ex)
        return False

    ch.setBusOutputControl(outputControl)
    ch.busOn()
    return ch


def tearDownChannel(ch):
    ch.busOff()
    ch.close()


ch0 = setUpChannel(channel=1)
# frame = Frame(
#     id_=100,
#     data=[1, 2, 3, 4],
#     flags=canlib.MessageFlag.EXT
# )
# ch1.write(frame)
if ch0:
    while True:
        try:
            frame = ch0.read()
            print(hex(frame.id), end='    ')
            for i in frame.data:
                print(hex(i), end=' ')
            print()
        except canlib.canNoMsg:
            print('No CAN')
            tearDownChannel(ch0)
        except canlib.canError as ex:
            print(ex)
            tearDownChannel(ch0)
