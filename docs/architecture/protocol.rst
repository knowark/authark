Protocol
--------

.. seqdiag::
   :desctable:

   seqdiag {
      # On initialization or refresh token expiration
      Consumer ->  Authark  [label = "POST /refresh-token
      {username,password}"];
      Consumer <-- Authark  [label = "{refresh_token}"];
      Consumer ->  Authark  [label = "POST /access-token
      {refresh_token}"];
      Consumer <-- Authark  [label = "{access_token}"];
      Consumer ->  Provider [label = "GET /resource
      {access_token}"];
      Consumer <-- Provider [label = "{data}"];
      
      # On access token expiration
      Consumer ->  Authark  [label = "POST /token\n{refresh_token}"];
      Consumer <-- Authark  [label = "{refresh_token}"];
      Consumer ->  Provider [label = "POST /resource\n{access_token, data}"];
      Consumer <-- Provider [label = "{ok}"];
      
      Consumer [description = "Client Application."];
      Authark [description = "Authentication Service."];
      Provider [description = "Resources Provider Server."];
   }

Authark's basic transactional protocol involves the generation of both an
**access token** and a **refresh token**. On initialization, the client
application sends a username and password to obtain an access and a refresh
token from Authark. By setting the access token on the **Authorization**
header, the client can retrieve data from protected resources and perform
actions over **secured providers**. When the access token has expired (
e.g. after 15 minutes) the client can use the refresh token (whose lifetime
spans for days or weeks) to issue a new set of tokens.
