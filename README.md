# Shop Now API's
Built a scalable e-commerce platform using Django and Django Rest Framework.
Enabled sellers to add products and manage discounts on specific product groups.
Developed a user-friendly interface for customers to add items to their cart, make purchases, and track their orders.
Integrated secure payment transactions using Razorpay.
Automated the delivery process by using Celery to change the order status to "delivered" once the delivery time has been reached.
Provided a solution for refunding the amount to the customer in case of returns within the guarantee period.
Followed test driven development, by using Unit testing to test.

### Implementation
- Django REST Framework function-based views
- Django REST Framework class-based views

Each of the implementations are tested and documented with OpenAPI (Swagger UI). 

### Local development
This project is heavily focused on the process of setting up the development environment. This project has been tested and developed on:

- Windows 11

### PEP8

This application follows PEP8 rules for styling and code readability.

### Developing with virtual environments

The application can be developed with a virtual environment locally. This requires starting RabbitMQ services locally.

### Setup Project

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/vvek475/Shop-Now.git
$ cd Shop-Now
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ pip install venv venv
$ venv/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
