from djitellopy import Tello

tello = Tello()
tello.connect()
tello.takeoff()
#
# # tello.move_left(100)
# tello.rotate_counter_clockwise(90)
# tello.move_forward(100)
#
# tello.land()

def move_left():
    tello.tello.rotate_counter_clockwise(1)

def move_right():
    tello.rotate_clockwise(1)

def landTello():
    tello.land()


if __name__ == "__main__":
    tello = Tello()
    tello.connect()
