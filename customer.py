from __future__ import print_function
import sys


class Customer(object):
    def __init__(self):
        self.order = [0, 1, 2, 3]

    def setName(self):
        while True:
            item = input("What's your name: ").strip()
            if item != "":
                break
            print("Please insert a name.")
        self.order[0] = item

    def setNumberOfMeals(self):
        item = 0
        while item <= 0:
            item = input("How many meals do you want: ").strip()
            # check its an int
            try:
                item = int(item)
            except:
                item = 0
                print("Please try again, and insert a valid number.")
                continue
            # checks its a valid int
            if item <= 0:
                print("Please try again, and insert a valid number.")
                item = 0
                continue

        self.order[1] = item

    def setHouseNumber(self):
        item = 0
        while item <= 0:
            item = input("What is your house number: ").strip()
            # check its an int
            try:
                item = int(item)
            except:
                item = 0
                print("Please try again, and insert a valid number.")
                continue
            # checks its a valid int
            if item <= 0:
                print("Please try again, and insert a valid number.")
                item = 0
                continue

        self.order[2] = item

    def setPostcode(self):
        item = input("Please insert your postcode: ").strip()
        # item.replace(" ", "")
        self.order[3] = item

    def sendOrder(self, server):
        # in sending we are asking a server to recieve a msg
        server.recieve("placeOrder", self.order)
        print()
        print(server.getResponse)
        print()
        print("Thank you for your order, Goodbye.")
