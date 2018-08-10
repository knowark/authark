Domain
------

Authark's objective is to simplify the authentication and authorization
process for a wide number of services. As such, the **User** model is at its
core, and so are the **Provider** and **Role**.


.. graphviz::

   digraph {
    graph [pad="0.5", nodesep="0.5", ranksep="2"];
    node [shape=plain]
    rankdir=LR;

    User [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>User</i></td></tr>
    <tr><td port="id">id</td></tr>
    </table>>];

    UserRole [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>UserRole</i></td></tr>
    <tr><td port="user_id">user_id</td></tr>
    <tr><td port="role_id">role_id</td></tr>
    </table>>];

    Role [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Role</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="provider_id">provider_id</td></tr>
    </table>>];

    Provider [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Provider</i></td></tr>
    <tr><td port="id">id</td></tr>
    </table>>];

    Resource [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Resource</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="provider_id">provider_id</td></tr>
    </table>>];

    Policy [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Policy</i></td></tr>
    <tr><td port="id">id</td></tr>
    </table>>];

    Permission [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Permission</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="resource_id">resource_id</td></tr> 
    <tr><td port="policy_id">policy_id</td></tr> 
    </table>>];

    UserRole:user_id -> User:id;
    UserRole:role_id -> Role:id;
    Role:provider_id -> Provider:id;
    Resource:provider_id -> Provider:id;
    Permission:resource_id -> Resource:id; 
    Permission:policy_id -> Policy:id;
    }


Providers can have multiple roles for authorization purposes, each been able
to hold multiple users. As a user can as well belong to multiple groups, the 
**UserRole** structure is the responsible of representing such binding.

A service or data **Provider** may have one or more **Resources** to which it
can give access. To do that, **Policies** are created to filter out the kind
of records a user can get access to, and a set of **Permissions** link them to
the specified **Resource**.