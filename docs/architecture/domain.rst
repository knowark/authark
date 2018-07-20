Domain
------

Authark's objective is to simplify the authentication and authorization
process for a wide number of services. As such, the **User** model is at its
core, and so are the **Provider** and **Group**.


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

    Role [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Role</i></td></tr>
    <tr><td port="user_id">user_id</td></tr>
    <tr><td port="group_id">group_id</td></tr>
    </table>>];

    Group [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Group</i></td></tr>
    <tr><td port="id">id</td></tr>
    <tr><td port="provider_id">provider_id</td></tr>
    </table>>];

    Membership [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Membership</i></td></tr>
    <tr><td port="provider_id">provider_id</td></tr>
    <tr><td port="user_id">user_id</td></tr>
    </table>>];

    Provider [label=<
    <table border="0" cellborder="1" cellspacing="0">
    <tr><td><i>Provider</i></td></tr>
    <tr><td port="id">id</td></tr>
    </table>>];

    Role:user_id -> User:id;
    Role:group_id -> Group:id;
    Membership:user_id -> User:id;
    Membership:provider_id -> Provider:id;
    Group:provider_id -> Provider:id;

    }

