import sys
import os

"""Variables prefixed with `DEFAULT` should be able to be overridden by
configuration file and command‐line arguments."""

UNIT = 100000000        # The same across assets.


# Versions
VERSION_MAJOR = 9
VERSION_MINOR = 47
VERSION_REVISION = 0
VERSION_STRING = str(VERSION_MAJOR) + '.' + str(VERSION_MINOR) + '.' + str(VERSION_REVISION)


# Counterparty protocol
TXTYPE_FORMAT = '>I'

TWO_WEEKS = 2 * 7 * 24 * 3600
MAX_EXPIRATION = 3600 * 60   # Two months

MEMPOOL_BLOCK_HASH = 'mempool'
MEMPOOL_BLOCK_INDEX = 9999999


# SQLite3
MAX_INT = 2**63 - 1


# Bitcoin Core
OP_RETURN_MAX_SIZE = 80 # bytes


# Currency agnosticism
BTC = 'VIA'
XCP = 'XCH'

BTC_NAME = 'Viacoin'
BTC_CLIENT = 'viacoind'
XCP_NAME = 'ClearingHouse'
XCP_CLIENT = 'clearinghoused'

DEFAULT_RPC_PORT_TESTNET = 17300
DEFAULT_RPC_PORT = 7300

DEFAULT_BACKEND_RPC_PORT_TESTNET = 25222
DEFAULT_BACKEND_RPC_PORT = 5222

UNSPENDABLE_TESTNET = 't7FjKY4NpTqUETtYCh1mrGwRMKzX9hkGd3'
UNSPENDABLE_MAINNET = 'Via2XCHoqQxACVuXf4vrajVDJetwVgxLMz'

ADDRESSVERSION_TESTNET = b'\x7f'
PRIVATEKEY_VERSION_TESTNET = b'\xff'
ADDRESSVERSION_MAINNET = b'\x47'
PRIVATEKEY_VERSION_MAINNET = b'\xc7'
MAGIC_BYTES_TESTNET = b'\xa9\xc5\xef\x92'   # For bip-0010
MAGIC_BYTES_MAINNET = b'\x0f\x68\xc6\xcb'   # For bip-0010

BLOCK_FIRST_TESTNET_TESTCOIN = 400000
BURN_START_TESTNET_TESTCOIN = 400000
BURN_END_TESTNET_TESTCOIN = 65700000     # Fifty years

BLOCK_FIRST_TESTNET = 400000
BLOCK_FIRST_TESTNET_HASH = 'b87e19be6fb5c2b3209274eea4c60f531ea3c0ec476550ec4dc161bd548acc62'
BURN_START_TESTNET = 400000
BURN_END_TESTNET = 65700000              # Fifty years, at ten minutes per block.

BLOCK_FIRST_MAINNET_TESTCOIN = 89100
BURN_START_MAINNET_TESTCOIN = 89100
BURN_END_MAINNET_TESTCOIN = 65700000     # A long time

BLOCK_FIRST_MAINNET = 86000
BLOCK_FIRST_MAINNET_HASH = 'a73aadfbf290b7bfca6089fdd5aef70ff0392f8024f94c9c5a855652f76a5169'
BURN_START_MAINNET = 89100
BURN_END_MAINNET = BURN_START_MAINNET + (3600 * 45)


# Protocol defaults
# NOTE: If the DUST_SIZE constants are changed, they MUST also be changed in xchblockd/lib/config.py as well
    # TODO: This should be updated, given their new configurability.
# TODO: The dust values should be lowered by 90%, once transactions with smaller outputs start confirming faster: <https://github.com/mastercoin-MSC/spec/issues/192>
DEFAULT_REGULAR_DUST_SIZE = 56000         # TODO: This is just a guess. I got it down to 5530 satoshis.
DEFAULT_MULTISIG_DUST_SIZE = 2 * 56000        # <https://bitcointalk.org/index.php?topic=528023.msg7469941#msg7469941>
DEFAULT_OP_RETURN_VALUE = 0
DEFAULT_FEE_PER_KB = 100000              # Viacoin Core default is 100000.


# UI defaults
DEFAULT_FEE_FRACTION_REQUIRED = .009   # 0.90%
DEFAULT_FEE_FRACTION_PROVIDED = .01    # 1.00%


# Custom exit codes
EXITCODE_UPDATE_REQUIRED = 5

CONSENSUS_HASH_SEED = 'We can only see a short distance ahead, but we can see plenty there that needs to be done.'

CONSENSUS_HASH_VERSION_MAINNET = 2
CHECKPOINTS_MAINNET = {
    BLOCK_FIRST_MAINNET: {'ledger_hash': '766ff0a9039521e3628a79fa669477ade241fc4c0ae541c3eae97f34b547b0b7', 'txlist_hash': '766ff0a9039521e3628a79fa669477ade241fc4c0ae541c3eae97f34b547b0b7'},
    400000: {'ledger_hash': 'f513bfeec7de32e40b1b8db2c480b999e59be77f994964651a52c83c993724d0', 'txlist_hash': '07c47d5ea69195760d9062975464ec83387e3fa0b99398c5fd551e6a3604f1f4'}
}

CONSENSUS_HASH_VERSION_TESTNET = 4
CHECKPOINTS_TESTNET = {
    BLOCK_FIRST_TESTNET: {'ledger_hash': 'aea33abbef46277f76a2ec040bc98bd0a27bab2a2210386bd5b48cc8d5cfe750', 'txlist_hash': 'aea33abbef46277f76a2ec040bc98bd0a27bab2a2210386bd5b48cc8d5cfe750'},
}
