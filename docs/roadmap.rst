Project Roadmap
###############


Version 1.0
===========

- [X] Login

  - [X] Add endpoint receiving a username and password
  - [X] Add 'auth' as an alias of 'login'
  - [X] Return an access token if authenticated
  - [X] Encode token

- [X] User registration

  - [X] Create endpoint for user registration 'register'
  - [ ] Create a 'users' endpoint
  - [ ] Persist users in json format with a encrypted password

- [ ] Credentials, Providers, Groups and Roles
  - [ ] Define Credentials
  - [ ] Define Providers
  - [ ] Define Groups
  - [ ] Define Roles

- [ ] Add basic security controls to Authark itself
  - [ ] Create default provider (i.e. Authark itself)
  - [ ] Create Authark's basic groups
  - [ ] Decode authentication token to use in Authark

- [X] Manage system's setup through configuration files 
- [X] Refactor to a standalone app by integrating gunicorn

Version 1.1
===========

- [ ] Add mypy file

- [ ] Ensure token expiration

Later
=====

- [ ] Use protocols instead of abstract base classes :D