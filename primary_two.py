from __future__ import print_function
import Pyro4
import sys
import postcodes_io_api


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Server(object):
    def __init__(self):
        self.orders = {}
        self.count = 0

    def store(self, name, numberOfMeals, houseNumber, postcode):
        # check the postcode validity
        api = postcodes_io_api.Api(debug_http=True)
        data = api.get_postcode(postcode)
        if data['status'] != 200:
            # send back info that its wrong
            try:
                frontEnd = Pyro4.Proxy("PYRONAME:front_end")
                frontEnd.checkOnline()
                msg = f"For order to: {name}\n{postcode} is not a valid postcode, please try again."
                self.send(frontEnd, "PostcodeERROR", msg)
                print()
                print("Order declined, invalid Postcode.")
                print()
            except:
                print("Front-end server is down.")
                print()
        else:
            postcode += '\n\t\t' + str(data['result']['primary_care_trust']) + '\n\t\t' + str(data['result']['region']) + '\n\t\t' + str(data['result']['country'])
            # print out details
            if numberOfMeals == 1:
                msg = f"\nOrder placed:\nCustomer: {name}\nOrder: {numberOfMeals} meal\nDelivering to: \n\t\tHouse Number {houseNumber}\n\t\t{postcode}"
            else:
                msg = f"\nOrder placed:\nCustomer: {name}\nOrder: {numberOfMeals} meals\nDelivering to: \n\t\tHouse Number {houseNumber}\n\t\t{postcode}"
            print(msg)

            # send confirmation to front end
            try:
                frontEnd = Pyro4.Proxy("PYRONAME:front_end")
                frontEnd.checkOnline()
                self.send(frontEnd, "confirmation", msg)
                print("Order confirmed.")
                print()
                # update our store once the order confirmed
                self.orders[self.count] = [name, numberOfMeals, houseNumber, postcode]
                self.count += 1
            except:
                print("Front-end server is down.")
                print()

            # update data across all servers
            try:
                self.attemptServersDataUpdate()
                print(f"Data updated across active servers.")
                print()
                # show the upated list
                print("Current list of orders confirmed:")
                for i in range(len(self.orders)):
                    print(f"Customer: {self.orders[i][0]}, Meals: {self.orders[i][1]}, Delivering to: \n\t\tHouse Number {self.orders[i][2]}\n\t\t{self.orders[i][3]}")
            except:
                pass
        print()
        print("Listening for new requests...")
        print()

    def checkOnline(self):
        return True

    def attemptServersDataUpdate(self):
        # send to primary 1
        try:
            p1 = Pyro4.Proxy("PYRONAME:primary1")
            p1.checkOnline()
            self.send(p1, "update", (self.count, self.orders))
        except:
            pass
        # send to primary 3
        try:
            p3 = Pyro4.Proxy("PYRONAME:primary3")
            p3.checkOnline()
            self.send(p3, "update", (self.count, self.orders))
        except:
            pass

    def send(self, server, msg1, msg2):
        # in sending we are asking a server to recieve a msg
        server.recieve(msg1, msg2)

    def recieve(self, msg1, msg2):
        if msg1 == "update":
            self.count = msg2[0]
            self.orders = msg2[1]
            msg = f"Server data has been updated."
            print(msg)
            print()
            # show the upated list
            print("Current list of orders confirmed:")
            for i in range(len(self.orders)):
                print(f"Customer: {self.orders[i][0]}, Meals: {self.orders[i][1]}, Delivering to: \n\t\tHouse Number {self.orders[i][2]}\n\t\t{self.orders[i][3]}")
        elif msg1 == "store":
            self.store(msg2[0], msg2[1], msg2[2], msg2[3])
        else:
            print("Unexpected return value")
            print()
            sys.exit()


def main():
    Pyro4.Daemon.serveSimple(
        {
            Server: "primary2"
        },
        ns=True)


if __name__ == "__main__":
    main()
