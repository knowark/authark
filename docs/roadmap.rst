Project Roadmap
###############


Version 1.0
===========

- [ ] Login

  - [X] Add endpoint receiving a username and password
  - [X] Add 'auth' as an alias of 'login'
  - [X] Return an access token if authenticated
  - [X] Encode token
  - [ ] Decode token

- [X] User registration

  - [X] Create endpoint for user registration 'register'

  - [ ] Create a 'users' endpoint

- [X] Refactor to a standalone app by integrating gunicorn

Version 1.1
===========

- [ ] Add mypy file

- [ ] Ensure token expiration

Later
=====

- [ ] Use protocols instead of abstract base classes :D