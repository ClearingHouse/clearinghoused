## Client Versions ##
* v9.47.1 (2014-12-01)
	* multi‐signature address support (protocol change: 490000)
	* numeric asset names (protocol change: 490000)
	* kickstart functionality
	* better process‐locking
	* improvements to documentation
	* graceful shutdown of processes
	* faster server startup
	* support for jmcorgan Bitcoin Core fork for block explorer
	* change first testnet block to 400000
	* make protocol changes always retroactive on testnet
* v9.47.0 (2014-11-19)
    * decode obfuscated OP_RETURN data
* v9.46.0 (2014-11-03)
	* new consensus hashes, with `tx_info` and consensus version
	* Coveralls support
	* rewrite of README
	* better multi‐sig address handling
	* multi‐sig change
	* use new process‐locking mechanism
	* use GitHub Pages for hosting minimum version information
	* bump versions of dependencies
	* miscellaneous clean up
* v9.45.0 (2014-11-13)
	* add dividend fee of 0.0002 XCH per recipient (protocol change: 420000)
* v9.44.0 (2014-11-13)
	* server action requires `server` positional argument
	* lockfile
	* made `--force` server‐side only, moved after `server` argument
	* multiple sources, destinations (testnet protocol change: 370000)
	* multi‐signature support (testnet protocol change: 370000)
* v9.43.1 (2014-11-13)
	* generate movements hash for each block (start at block: 400000)
* v9.43.0 (2014-10-05)
	* enable blockchain notary (protocol change: 275000)
* v9.42.0 (2014-09-04)
	* disable dividends to XCP holders (protocol change: 193000)
	* allow dividends only from issuers (protocol change: 193000)
* v9.41.1 (2014-08-28)
	* Increase order-match period (protocol change 150000)
* v9.41.0 (2014-08-21)
	* fixed bug in new text and descriptions
* v9.40.0 (2014-08-20)
	* allow dividends to be paid to XCH holders (protocol change: 125000)
	* fixed bug in VIApay validation
	* allow null expirations (protocol change: 125000)
	* assert first block in database is BLOCK_FIRST
	* arbitrarily long asset descriptions and broadcast texts (protocol change: 125000)
	* don’t close order matches when penalizing (protocol change: 125000)
* v9.39.0 (2014-08-12)
	* re‐match expired order matches from a new block all at once (protocol change: 95000)
	* bug in issuance fee (protocol change: 95000/31500)
* v9.38.0 (2014-08-11)
    * Initial release
