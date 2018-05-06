.. Authark documentation master file, created by
   sphinx-quickstart on Sun May  6 10:28:33 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Authark (0.1.0)
===============

Authentication and authorization server.

**NOTE:** *Under Development - Not Production Ready*

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   architecture.rst
   roadmap.rst
   about.rst

Design
------

*Authark* is designed to return an authentication *token* when
authentication against it is successful. A *private secret* should be shared
among all the *applications* that would like to use Authark as their
authentication and authorization server.

Usage
-----

To run authark you should use gunicorn or any other wsgi compatible
http server.

For example:

```
gunicorn authark.main:app
```

You can register a new account by posting to the */register* endpoint
providing a *username* and *password* in a *json* document.

To get a *token*, use the */login* or */auth* endpoint. This token is
generated from a *private secret* that should be *shared* between
*Authark* and the *protected resource applications*.
