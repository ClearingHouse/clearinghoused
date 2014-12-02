#! /usr/bin/python3

"""
Create notary documents.
"""

import struct
import decimal
import binascii

from lib import (config, util, exceptions, bitcoin, util)

# H:HASH_TYPE
# 32s: HASH

FORMAT = '>H32s'
LENGTH_SHA2 = 2 + 32

ID=160

def validate (db, source, hash_type, hash_string, description, block_index):
    problems = []

    if hash_type != 0:
        problems.append("Only hash-type 0 (SHA2) supported.")

    if len(hash_string) != 64:
        problems.append("Not a valid SHA2 hash.")

    # TODO: Add check for description length

    cursor = db.cursor()

    documents = list(cursor.execute('''SELECT * FROM documents WHERE (hash_string = ? AND hash_type = ?)''', (hash_string, hash_type)))
    if documents:
        problems.append("Document is already submitted.")

    cursor.close()
    return hash_type, hash_string, description, block_index, problems

def parse (db, tx, message):
    notary_parse_cursor = db.cursor()
    status = 'valid'

    try:
        if tx['block_index'] >= 275000 or config.TESTNET:  # protocol change
            length = len(message) - LENGTH_SHA2
            if length == 0:
                notary_format = FORMAT
                hash_type, hash_bytes = struct.unpack(notary_format, message)
                description = ''
            else:
                notary_format = FORMAT + '{}s'.format(length)
                hash_type, hash_bytes, description = struct.unpack(notary_format, message)
                try:
                    description = description.decode('utf-8')
                except UnicodeDecodeError:
                    description = ''

            #raise exceptions.NotaryIssuanceError("FORMAT: {}, message: {}, LEN(message) {}, LENGTH_SHA2 {}, length: {}", notary_format, message, len(message), LENGTH_SHA2, length)
            hash_string = binascii.hexlify(hash_bytes).decode('utf-8')
        else:
            assert False
    except (AssertionError, struct.error) as e:
        #raise exceptions.NotaryIssuanceError("error: {}, message: {} and notary_format: {}",e, message, notary_format)
        hash_type, hash_string, description= None, None, None
        status = 'invalid'

    if not hash_string:
        status = 'invalid'

    if status != 'invalid':
        hash_type, hash_string, description, block_index, problems = validate(db, tx['source'], hash_type, hash_string, description, tx['block_index'])
        if problems:
            status = 'invalid'

    if status == 'valid':
        # Add parsed transaction to message-type–specific table.

        # Update transaction log
        bindings = {
            'tx_index': tx['tx_index'],
            'tx_hash': tx['tx_hash'],
            'block_index': tx['block_index'],
            'source': tx['source'],
            'destination': tx['source'],
            'hash_type': hash_type,
            'hash_string': hash_string
        }

        sql='INSERT INTO document_transactions VALUES(:tx_index, :tx_hash, :block_index, :source, :destination, :hash_type, :hash_string)'
        notary_parse_cursor.execute(sql, bindings)

        # Update document state for quick lookups
        bindings = {
            'owner': tx['source'],
            'hash_string': hash_string,
            'hash_type': hash_type,
            'block_index': tx['block_index'],
            'description': description,
            'tx_hash': tx['tx_hash']
        }
        sql='INSERT INTO documents VALUES(:owner, :hash_string, :hash_type, :description, :tx_hash)'
        notary_parse_cursor.execute(sql, bindings)

    notary_parse_cursor.close()

def compose (db, source, hash_type, hash_string, description):
    hash_type, hash_string, description, block_index, problems = validate(db, source, hash_type, hash_string, description, util.last_block(db)['block_index'])
    if problems:
        raise exceptions.NotaryIssuanceError(problems)

    if not description:
        description = ''

    pack_format = FORMAT + '{}s'.format(len(description))
    data = struct.pack(config.TXTYPE_FORMAT, ID)
    string_bytes = binascii.unhexlify(bytes(hash_string, 'utf-8'))
    data += struct.pack(pack_format, hash_type, string_bytes, description.encode('utf-8'))

    return (source,[], data)

