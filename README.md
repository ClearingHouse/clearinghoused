[![Build Status](https://travis-ci.org/CounterpartyXCP/counterpartyd.svg?branch=develop)](https://travis-ci.org/CounterpartyXCP/counterpartyd)
[![Coverage Status](https://coveralls.io/repos/CounterpartyXCP/counterpartyd/badge.png?branch=develop)](https://coveralls.io/r/CounterpartyXCP/counterpartyd?branch=develop)

# Description
`clearinghoused` is the reference implementation of the [ClearingHouse
Protocol](https://github.com/ClearingHouse/ClearingHouse).


# Dependencies
* [Python 3](http://python.org)
* [Python 3 packages](https://github.com/ClearingHouse/clearinghoused/blob/master/pip-requirements.txt)
* Viacoin Core

Sometimes the underlying package requirements may change for `clearinghoused`.
If you build and installed it from scratch, you can manually update these
requirements by executing something like:
```
    pip3 install --upgrade -r pip-requirements.txt 
```

# Versioning
* Major version changes require a full (automatic) rebuild of the database.
* Minor version changes require a(n automatic) database reparse.
* Most protocol changes are retroactive on testnet.


# Installation

**NOTE: This section covers manual installation of clearinghoused. If you want more of
an automated approach to clearinghoused installation for Windows and Linux, use
the [build system](http://clearinghouse.io/docs/build-system/).**

In order for clearinghoused to function, it must be able to communicate with a
running instance of Viacoin Core, which handles many Viacoin‐specific matters
on its behalf, including all wallet and private key management. For such
interoperability, Viacoin Core must be run with the following options: `-txindex=1`
`-server=1`. This may require the setting of a JSON‐RPC password, which may be
saved in Viacoin Core’s configuration file.

clearinghoused needs to know at least the JSON‐RPC password of the Viacoin Core
with which it is supposed to communicate. The simplest way to set this is to
include it in all command‐line invocations of counterpartyd, such as
`./counterpartyd.py --rpc-password=PASSWORD ACTION`. To make this and other
options persistent across counterpartyd sessions, one may store the desired
settings in a configuration file specific to clearinghoused.

Note that the syntaxes for the clearinghoused and the Viacoin Core configuraion
files are not the same. A Viacoin Core configuration file looks like this:

	rpcuser=viacoinrpc
	rpcpassword=PASSWORD
	testnet=1
	txindex=1
	server=1

However, a clearinghoused configuration file looks like this:

	[Default]
	backend-rpc-password=PASSWORD

Note the change in hyphenation between `rpcpassword` and `rpc-password`.

If and only if clearinghoused is to be run on the Viacoin testnet, with the
`--testnet` CLI option, Viacoin Core must be set to do the same (`-testnet=1`).
clearinghoused may run with the `--testcoin` option on any blockchain,
however.


# Usage
The command‐line syntax of clearinghoused is generally that of
`./clearinghoused.py {OPTIONS} ACTION {ACTION-OPTIONS}`. There is a one action
per message type, which action produces and broadcasts such a message; the
message parameters are specified following the name of the message type. There
are also actions which do not correspond to message types, but rather exist to
provide information about the state of the Counterparty network, e.g. current
balances or open orders.

For a summary of the command‐line arguments and options, see
`./clearinghoused.py --help`.

The test suite is invoked with `py.test` in the root directory of the repository.


### Input and Output
* Quantities of divisible assets are written to eight decimal places.
* Quantities of indivisible assets are written as integers.
* All other quantities, i.e. prices, odds, leverages, feed values and target
values, fee multipliers, are represented internally as fractions, but printed
to four decimal places.


### Example Usage
The following examples are abridged for parsimony.

* Server

	The `server` command should always be running in the background (or another console). All other commands will fail if the index of the last block in the database is less than that of the last block seen by Viacoin Core.

* Burn

	`burn --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --quantity=.5`

* Send divisible or indivisible assets

	```
	send --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --quantity=3 --asset=BBBC
	--to=t3BrDB6zDiEPWEE6wLxywFb4Yp9ZY5fHM7
	```

* Buy VIA for XCH

	```
	order --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --get-quantity=10 --get-asset=VIA
	--give-quantity=20 --give-asset=XCH --expiration=10 --fee=.001
	```

* Buy BBBC for VIA

	```
	order --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --get-quantity=10 --get-asset=BBBC
	--give-quantity=20 --give-asset=VIA --expiration=10 --fee=0.001
	```

* Buy XCH for BBBC
 
	```
	order --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --get-quantity=10 --get-asset=XCH
	--give-quantity=20 --give-asset=BBBC --expiration=10
	```

* VIAPay

	```
	btcpay --source=mtQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --order-match-id=092f15d36786136c4d868c33356ec3c9b5a0c77de54ed0e96a8dbdd8af160c23
	```
	Order Match ID can be obtained with the `pending` command.

* Issue

	`issuance --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --quantity=100 --asset='BBBC'`

	`issuance --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --quantity=100 --asset='BBBQ' --divisible`

* Broadcast

	```
	broadcast --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --text="Viacoin price feed" --value=825.22
	--fee-multiplier=0.001
	```

	Note: for some users clearinghoused has trouble parsing spaces in the `--text` argument. One workaround is to
		add an additional set of quotes. For example, `--text='"Viacoin price feed"'`.

* Bet
	
	Equal/Not Equal Bet:
	
	Example: Bet on Super Bowl Feed. Denver vs. Seattle. Feed value of 1 means Seattle Wins. Feed value of 2 means
	Denver Wins. This command places a 1 XCH bet on the Super Bowl Feed for Seattle to win, paying out 2 to
	1. The bet will expire in 100 blocks and the settlement value of the bet is based on the first feed
	update after the deadline timestamp of February 3, 2014 1:39 PM US Eastern Standard Time (UTC-0500)
	```
	bet --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --feed-address=t3BrDB6zDiEPWEE6wLxywFb4Yp9ZY5fH --bet-type=Equal
	--deadline=2014-02-03T13:39:00-0500 --wager=1 --counterwager=2 --target-value=1 --expiration=100
	```

	Contract for Difference:
	
	Example: Bet on Viacoin Price Feed. This command places a bearish (short) 1 XCH wager on the price of VIA/USD 				
	with 2X leverage. The bet will expire in 100 blocks and the settlement value of the bet is based 			
	on the first feed update after the deadline timestamp of February 3, 2014 1:39 PM US Eastern 					
	Standard Time (UTC-0500)
	```
	bet --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --feed-address=t3BrDB6zDiEPWEE6wLxywFb4Yp9ZY5fH --bet-type=BearCFD --deadline=2014-02-03T13:39:00-0500 --wager=1 --counterwager=1 --leverage=10080 --expiration=100
	```

* Rock-Paper-Scissors
	
	Open a Rock-Paper-Scissors like game with arbitrary possible moves (Must be an odd number greater or equal than 3). 
	Until you make an rpsresolve transaction, your move is stored as an hash and keep secret.
	
	Example: Play [rock-paper-scissors-spock-lizard](http://en.wikipedia.org/wiki/Rock-paper-scissors-lizard-Spock):

	```
	rps --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --possible-moves=5 --move=2 --wager=1 --expiration=100
	```

	Keep well the random number generated, you need it to resolve the game after matching:
	
	```
	rpsresolve --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --move=2 --random=adc5eadf9cb698ff6f2410d76131a4ee --rps-match-id=c68ffe144952977b94f8d7b49a1c7be7a4bb522c56f2ffc5aefa78ae0f9799b003b0f79d59ba660138583277b8267301a1030577790b945c4e8f845f19c23ca2
	```

* Cancel
	```
	cancel --source=mtQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --offer-hash=092f15d36786136c4d868c33356ec3c9b5a0c77de54ed0e96a8dbdd8af160c23
	```

* Dividend
	```
	dividend --source=ttQheFaSfWELRB2MyMBaiWjdDm6ux9Ezns --quantity-per-share=1 --asset=MULTIPOOLSTOCK
	```

* Market

	The `market` action prints out tables of open orders, open bets, feeds, and order matches currently awaiting 	        
	Viacoin payments from one of your addresses. 
	
	It is capable of filtering orders by assets to be bought and sold.
	
	Example:
	
	To filter the market to only show offers to sell (give) VIA:
	```
	market --give-asset=VIA
	```
	
	To filter the market to only show offers to buy (get) VIA:
	```
	market --get-asset=VIA
	```
	
	To filter the market to only show offers to sell VIA for XCH:
	```
	market --give-asset=VIA --get-asset=XCH
	```

* Asset

	The `asset` action displays the basic properties of a given asset.

* Address

	The `address` action displays the details of of all transactions involving the ClearingHouse address which is its argument.

