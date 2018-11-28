Domain
------

Authark's objective is to simplify the authentication and authorization
process for a wide number of services. As such, the **User** model is at its
core, and so are the **Dominion** and **Role**.


.. graphviz::

   digraph {
    graph [pad="0.5", nodesep="0.5", ranksep="2"];
    node [shape=plain]
    rankdir=LR;

    Token [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Token</i></td></tr>
    <tr><td port="value">value</td></tr>
    </table>>];

    User [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>User</i></td></tr>
    <tr><td port="id">id</td></tr>
    </table>>];
    
    Attribute [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Attribute</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="user_id">user_id</td></tr>
    </table>>];

    Ranking [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Ranking</i></td></tr>
    <tr><td port="user_id">user_id</td></tr>
    <tr><td port="role_id">role_id</td></tr>
    </table>>];

    Credential [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Credential</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="dominion_id">dominion_id</td></tr>
    <tr><td port="user_id">user_id</td></tr>
    <tr><td port="client">client</td></tr>
    <tr><td port="type">type</td></tr>
    <tr><td port="value">value</td></tr>
    </table>>];

    Role [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Role</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="dominion_id">dominion_id</td></tr>
    </table>>];

    Dominion [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Dominion</i></td></tr>
    <tr><td port="id">id</td></tr>
    </table>>];

    Resource [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Resource</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="dominion_id">dominion_id</td></tr>
    </table>>];

    Policy [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Policy</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="type">type</td></tr> 
    <tr><td port="user_id">user_id (nullable)</td></tr>  
    <tr><td port="role_id">role_id (nullable)</td></tr>
    <tr><td port="value">value</td></tr>
    </table>>];

    Permission [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Permission</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="match">match</td></tr> 
    <tr><td port="resource_id">resource_id</td></tr> 
    <tr><td port="policy_id">policy_id</td></tr> 
    </table>>];

    RolePermission [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>RolePermission</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="permission_id">permission_id</td></tr>
    <tr><td port="role_id">role_id</td></tr> 
    </table>>];

    Attribute:user_id -> User:id;
    Ranking:user_id -> User:id;
    Ranking:role_id -> Role:id;
    Credential:dominion_id ->  Dominion:id;
    Credential:user_id -> User:id;
    Role:dominion_id -> Dominion:id;
    Resource:dominion_id -> Dominion:id;
    Permission:resource_id -> Resource:id; 
    Permission:policy_id -> Policy:id;
    RolePermission:role_id -> Role:id;
    RolePermission:permission_id -> Permission:id;
    Policy:user_id -> User:id;
    Policy:role_id -> Role:id;
    }


Dominions can have multiple roles for authorization purposes, each been able
to hold multiple users. As a user can as well belong to multiple groups, the 
**Ranking** structure is the responsible of representing such binding. A user
may have multiple **Credentials** to authenticate against Authark. Each 
**Credential** must be either of the type 'password' or 'token' (i.e. refresh
token) and belong to a single **Dominion**. Moreover, **Users** may have
optional **Attributes** in the form of *key-value* pairs that represent
any kind of informative features or data suitable for authorization logic.

A service or data **Dominion** may have one or more **Resources** to which it
can give access. To do that, **Policies** are created to filter out the kind
of records a user can get access to, and a set of **Permissions** link them to
the specified **Resource**.

The **Policy** type may be one of *user*, *role*, *time* or *domain*.
**Permissions** should define a *match* attribute which can be *all* or *any*.

**Tokens** are issued as value objects by Authark in return of a successful
authentication transaction initiated by a Client application. This **Token**
will be used independently and in a stateless manner to concede access to
protected applications and resources using **Authark** as their authentication
and authorization server.
