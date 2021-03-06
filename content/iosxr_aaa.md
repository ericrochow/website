Title: AAA on IOX-XR
Date: 2019-09-06 14:34
Category: Network
Tags: ios-xr, authentication, cli
Authors: Eric Rochow
Summary: A quick primer on how to configure authentication on IOS-XR

# AAA

## Authentication Methods

### Local

NOTE: Local users and groups are stored in a local database and not in the running configuration so they will not show up in ``show run`` output.

#### Define a new task group

        taskgroup $groupname
         description $description
         inherit taskgroup $taskgroup
         task $permission $taskname

#### Define a new user group

If the pre-defined user groups do not suffice, it is possible to configure customized user groups more more granularity with permissions:

        usergroup $groupname 
         description $description
         taskgroup $taskgroup
         inherit usergroup $groupname

#### Define a new user

        username $user
         group $groupname
         secret 0 $plaintext_password

### RADIUS

#### Configure servers

        radius source-interface $interface vrf default
        radius-server host $server1_ip auth-port 1812 acct-port 1813 
         key 7 $secret_key
        !
        radius-server host $server2_ip auth-port 1812 acct-port 1813
         key 7 $secret_key
        !
        radius-server timeout 20
        radius-server deadtime 5
        radius-server dead-criteria time 8
        radius-server dead-criteria tries 3

#### Configure AAA

        aaa accounting exec default start-stop group $server-group
        aaa accounting system default start-stop group $server-group
        aaa group server radius $server-group 
         server $server1_ip auth-port 1812 acct-port 1813 
         server $server2_ip auth-port 1812 acct-port 1813
         deadtime 10 
         source-interface $interface
        !
        aaa authentication login default local group $server-group

### TACACS+

        aaa group server tacacs+ $groupname
         server $server1_ip
         server $server2_ip
        aaa authentication login default local group $server-group
        aaa authorization commands default local tacacs+
        aaa accounting exec default start-stop group $server-group
        aaa accounting system default start-stop group $server-group


## Activate AAA

### SSH

If a AAA group besides 'default' is used (e.g. aaa authentication login my-list), then the list will need to be added to the appropriate lines:

        line default
         authorization commands default
         authorization exec default
         
### Console

        line console
         authorization commands default
         authorization exec default
