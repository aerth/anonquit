# Anonquit

### By fanta

Creative Commons Attribution 4.0 International

Anonquit is a program written in python3 used to publish in gnusocial (eg in this node http://gnusocial.net ) and can handle multiple user accounts.

Apart from publishing leaving our IP you can be published by passing through the Tor network if you have installed on your system tor. Thus the IP that will remain in the node server will be a different from ours.

dependencies:

    python3
    curl 

To set up an account:

```

  anonquit -a 

```

We ask the user node and password. It is saved plaintext in a sqlite database located at ~/.config/anonquit/anonquit.db

The password is not displayed but is being written. Once you press enter warns us that the account was created and we can start using it.


## Post on GNU Social with Python and cURL

  anonquit -u fanta@gnusocial.net "Hello world from anonquit" 

## Post something through the Tor network:

  anonquit -u fanta@gnusocial.net "anonquit first message through the Tor network" -t

## Delete account from local database

  anonquit -d 

We will ask the user and node and that account will be deleted.


```
Anyway. The code is a potato and I've created quickly in a few hours but it works more or less (at least to me). Now try taking more and go hit and especially to pass function many of the things that are repeated.

In version 0.2 the thing needs to improve. If used anonquit and find faults (that will) feel free to comment here to go can solve them.

Enjoy and remember:

    "A man is not sincere when he speaks of himself, give him a mask and tell the truth." 

Velvet Goldmine - 1998 film directed by Todd Haynes.

Use your mascara for good :). 
```
