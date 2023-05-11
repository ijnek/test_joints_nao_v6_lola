#!/usr/bin/env python3

import socket
import msgpack

class Robot:
    def __init__(self):
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.connect("/tmp/robocup")
        self.joints = [
            "HeadYaw",
            "HeadPitch",
            "LShoulderPitch",
            "LShoulderRoll",
            "LElbowYaw",
            "LElbowRoll",
            "LWristYaw",
            "LHipYawPitch",
            "LHipRoll",
            "LHipPitch",
            "LKneePitch",
            "LAnklePitch",
            "LAnkleRoll",
            "RHipRoll",
            "RHipPitch",
            "RKneePitch",
            "RAnklePitch",
            "RAnkleRoll",
            "RShoulderPitch",
            "RShoulderRoll",
            "RElbowYaw",
            "RElbowRoll",
            "RWristYaw",
            "LHand",
            "RHand"
        ]
        self.sonars = [
            "Left",
            "Right",
        ]
        self.touch = [
            "ChestBoard/Button",
            "Head/Touch/Front",
            "Head/Touch/Middle",
            "Head/Touch/Rear",
            "LFoot/Bumper/Left",
            "LFoot/Bumper/Right",
            "LHand/Touch/Back",
            "LHand/Touch/Left",
            "LHand/Touch/Right",
            "RFoot/Bumper/Left",
            "RFoot/Bumper/Right",
            "RHand/Touch/Back",
            "RHand/Touch/Left",
            "RHand/Touch/Right",
        ]
        self.LEar = [
            "0",
            "36",
            "72",
            "108",
            "144",
            "180",
            "216",
            "252",
            "288",
            "324"
        ]
        self.REar = [
            "324",
            "288",
            "252",
            "216",
            "180",
            "144",
            "108",
            "72",
            "36",
            "0"
        ]
        self.actuators = {
            'Position': self.joints,
            'Stiffness': self.joints,
            'Chest': ['Red', 'Green', 'Blue'],
            'Sonar': self.sonars,
            'LEar': self.LEar,
            'REar': self.REar
        }
        self.commands = {
            'Position': [0.0]*25,
            'Stiffness': [0.0]*25,
            'Chest': [0.0]*3,
            'Sonar': [True, True],
            'LEar': [0.0]*10,
            'REar': [0.0]*10
        }

    def read(self):
        stream = self.socket.recv(896)
        upacker = msgpack.unpackb(stream)
        return upacker

    def command(self, category, device, value):
        self.commands[category][self.actuators[category].index(device)] = value

    def send(self):
        stream = msgpack.packb(self.commands)
        self.socket.send(stream)

    def close(self):
        self.socket.close()

def main():
    robot = Robot()
    try:
        while True:
            robot.command("Position", "HeadYaw", 1.57)
            robot.command("Stiffness", "HeadYaw", 1.00)
            robot.send()
    except KeyboardInterrupt:
        print("Exit")
    finally:
        robot.close()

if __name__ == "__main__":
    main()
