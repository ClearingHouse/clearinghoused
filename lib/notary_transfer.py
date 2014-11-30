#! /usr/bin/python3

"""
Transfer document ownership
"""

import struct
import decimal
import binascii

from . import (config, util, exceptions, bitcoin, util)

# H:HASH_TYPE
# 32s: HASH

FORMAT = '>H32s'
LENGTH_SHA2 = 2 + 32

ID=161

def validate (db, source, hash_type, hash_string, block_index, destination):
    problems = []

    if hash_type != 0:
        problems.append("Only hash-type 0 (SHA2) supported.")

    if len(hash_string) != 64:
        problems.append("Not a valid SHA2 hash.")

    if not destination:
        problems.append("No destination given")

    if source == destination:
        problems.append("You can't transfer ownership to the current owner.")

    cursor = db.cursor()
    documents = list(cursor.execute('''SELECT * FROM documents WHERE (hash_string = ? AND hash_type = ?) AND owner = ?''', (hash_string, hash_type, source)))
    cursor.close()

    if not documents:
        problems.append("You don't own this document or the document does not exist.")

    return hash_type, hash_string, block_index, destination, problems

def parse (db, tx, message):
    status = 'valid'

    try:
        if tx['block_index'] >= 275000 or config.TESTNET:
            hash_type, hash_bytes = struct.unpack(FORMAT, message)
            hash_string = binascii.hexlify(hash_bytes).decode('utf-8')
        else:
            assert False
    except (AssertionError, struct.error) as e:
        hash_type, hash_string = None, None
        status = 'invalid'

    if status != 'invalid':
        hash_type, hash_string, block_index, destination, problems = validate(db, tx['source'], hash_type, hash_string, tx['block_index'], tx['destination'])

        if problems:
            status = 'invalid'

    if status == 'valid':
        notarytx_cursor = db.cursor()
        bindings = {
            'tx_index': tx['tx_index'],
            'tx_hash': tx['tx_hash'],
            'block_index': tx['block_index'],
            'source': tx['source'],
            'destination': destination,
            'hash_type': hash_type,
            'hash_string': hash_string
        }
        sql='insert into document_transactions VALUES(:tx_index, :tx_hash, :block_index, :source, :destination, :hash_type, :hash_string)'
        notarytx_cursor.execute(sql, bindings)
        notarytx_cursor.close()

        # I know we are not using the block_index here but if we remove it things, well break down. So keep it in here.
        notarytx_cursor = db.cursor()
        bindings = {
            'owner': destination,
            'tx_hash': tx['tx_hash'],
            'hash_type': hash_type,
            'hash_string': hash_string,
            'block_index': tx['block_index']
        }
        sql='update documents SET owner = :owner, tx_hash = :tx_hash WHERE hash_type = :hash_type AND hash_string = :hash_string'

        notarytx_cursor.execute(sql, bindings)
        notarytx_cursor.close()


def compose (db, source, destination, hash_type, hash_string):
    hash_type, hash_string,block_index,destination, problems = validate(db, source, hash_type, hash_string, util.last_block(db)['block_index'], destination)
    if problems:
        raise exceptions.NotaryTransferError(problems)

    data = struct.pack(config.TXTYPE_FORMAT, ID)
    string_bytes = binascii.unhexlify(bytes(hash_string, 'utf-8'))
    data += struct.pack(FORMAT, hash_type, string_bytes)

    return (source,[(destination, None)], data)

