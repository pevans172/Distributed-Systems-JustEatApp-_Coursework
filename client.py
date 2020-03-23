import sys
import Pyro4
import Pyro4.util
from customer import Customer

sys.excepthook = Pyro4.util.excepthook
# check that the front-end is online
try:
    frontEnd = Pyro4.Proxy("PYRONAME:front_end")
    frontEnd.checkOnline()
except:
    print("Server is down, please try again later.")
    print()
    sys.exit()

try:
    # attempt to send an order
    customer = Customer()
    print()
    customer.setName()
    customer.setNumberOfMeals()
    customer.setHouseNumber()
    customer.setPostcode()
    customer.sendOrder(frontEnd)
except:
    # end when there is an error
    print("Server is down, please try again later.")
    print()

# python -m Pyro4.naming
# python -m Pyro4.nsc list
