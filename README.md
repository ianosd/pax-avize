# pax-avize

This app allows store operators to create a product list (an order, ro: "aviz") for clients shopping in their store, and sending it to the
cashier once it is ready. The cashier can then easily drag-and-drop the order into the commerce-management software SAGA C,
which is the software managing the cash register. (you are welcome to integrate this with your own financial software)

The motivation for developing this app was to efficientize the cash-in process in a hardware-store, where
these orders used to be written on paper, and given to the cashier to input into SAGA C by hand. This was error-prone
and led to unnecessary waiting times.

## Components

The app has three components: a frontend for the operator, wher he inputs orders, a frontend for the cashier, which is actually
an `electron` app built from the same code as the operator frontend the two residing in the directory `frontend`.

In the folder `backend` resides a python server (implemented using `bottle`) which manages the incoming orders and also serves
data about the products.
