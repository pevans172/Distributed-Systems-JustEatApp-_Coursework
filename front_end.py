from __future__ import print_function
import Pyro4
import sys


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server(object):
    def __init__(self):
        self._response = ""

    def checkOnline(self):
        return True

    def findPrimary(self):
        # get primary 1
        try:
            primary = Pyro4.Proxy("PYRONAME:primary1")
            primary.checkOnline()
            return primary
        except:
            pass
        # get primary 2
        try:
            primary = Pyro4.Proxy("PYRONAME:primary2")
            primary.checkOnline()
            return primary
        except:
            pass
        # get primary 3
        try:
            primary = Pyro4.Proxy("PYRONAME:primary3")
            primary.checkOnline()
            return primary
        except:
            pass
        # reached if no server is online
        return False

    def placeOrder(self, order):
        while True:
            primary = self.findPrimary()
            try:
                if not primary:
                    print("All servers are down.")
                    print()
                    self._response = "All servers are down, try again soon."
                    break
                else:
                    self.send(primary, "store", order)
                    break
            except:
                print("Unexpected server shutdown, switch to next primary")
                print()

    def send(self, server, msg1, msg2):
        # in sending we are asking a server to recieve a msg
        server.recieve(msg1, msg2)

    def recieve(self, msg1, msg2):
        if msg1 == "placeOrder":
            msg = f"Order recieved for Customer: {msg2[0]}\nSending to current Primary server for processing."
            print(msg)
            print()
            self.placeOrder(msg2)
        elif msg1 == "confirmation":
            print("Order confirmed ->")
            print(msg2)
            print()
            self._response = msg2
            print()
            print("Listening for new requests...")
            print()
        elif msg1 == "PostcodeERROR":
            print(msg2)
            print()
            self._response = msg2
            print()
            print("Listening for new requests...")
            print()
        else:
            print(msg2)
            print()
            self._response = msg2
            print()
            print("Listening for new requests...")
            print()

    @property
    def getResponse(self):
        return self._response


def main():
    Pyro4.Daemon.serveSimple(
        {
            Server: "front_end"
        },
        ns=True)


if __name__ == "__main__":
    main()
