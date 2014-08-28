import decimal
import time
from lib import config, exceptions
# Full name to resolve circular dependency
import lib.bitcoin

def check():
    pass

def getinfo():
    pass

def getmempool():
    rawtxlist = lib.bitcoin.rpc('getrawmempool', [])
    txlist = []
    for rawtx in rawtxlist:
        try:
            txlist.append(lib.bitcoin.rpc('getrawtransaction', [rawtx]))
        except exceptions.RPCError:
            pass
    rv = [lib.bitcoin.rpc('decoderawtransaction', [tx]) for tx in txlist]
    for tx in rv:
        tx['confirmations'] = 0
    return rv

def searchrawtx(address):
    rv = []
    idx = 0
    while True:
        chunk = lib.bitcoin.rpc('searchrawtransactions', [address, 1, idx])
        if not chunk:
            break
        rv += [t for t in chunk if 'confirmations' in t and t['confirmations']]
        idx += 100
    return rv

def ismine(vout, address, allow_multisig=False):
    return 'scriptPubKey' in vout and \
           (allow_multisig or vout['scriptPubKey']['type'] != 'multisig') and \
           'addresses' in vout['scriptPubKey'] and \
           address in vout['scriptPubKey']['addresses']

def has_my_vout(tx, address):
    for vout in tx['vout']:
        if ismine(vout, address):
            return True
    return False

def has_my_vin(tx, vout_txs, address):
    for vin in tx['vin']:
        if vin['txid'] in vout_txs:
            for vout in vout_txs[vin['txid']]:
                if vout['n'] == vin['vout'] and ismine(vout, address):
                    return True
    return False

def locate_vout(vouts, n):
    for vout in vouts:
        if vout['n'] == n:
            return vout
    return None

def listunspent(address):
    # TODO p2sh
    txraw = getmempool() + searchrawtx(address)
    txs = {tx['txid']: tx for tx in txraw}
    for txid in txs:
        for vin in txs[txid]['vin']:
            if vin['txid'] in txs:
                txs[vin['txid']]['vout'] = [v for v in txs[vin['txid']]['vout'] if v['n'] != vin['vout']]
    for txid in txs:
        txs[txid]['vout'] = [v for v in txs[txid]['vout'] if ismine(v, address)]

    rv = []
    for txid in txs:
        for vout in txs[txid]['vout']:
            rv.append({'address': address,
                       'txid': txid,
                       'vout': vout['n'],
                       'ts': txs[txid]['time'] if 'time' in txs[txid] else int(time.time()),
                       'scriptPubKey': vout['scriptPubKey']['hex'],
                       'amount': vout['value'],
                       'confirmations': txs[txid]['confirmations']})
    return rv


def getaddressinfo(address):
    totalReceived = decimal.Decimal(0.0)
    totalSent = decimal.Decimal(0.0)
    unconfirmedBalance = decimal.Decimal(0.0)
    unconfirmedTxApperances = 0
    txApperances = 0

    mempool = getmempool()
    mptxs = {tx['txid']: tx for tx in mempool}
    txraw = searchrawtx(address)
    txs = {tx['txid']: tx for tx in txraw}

    # collect mempool incoming
    mptxs_own_vouts = {mptx: mptxs[mptx] for mptx in mptxs if mptx not in txs and has_my_vout(mptxs[mptx], address)}

    # collect mempool outgoing
    mptxs_own_vins = {}
    for mptx in mptxs:
        if mptx in txs:
            continue
        for vin in mptxs[mptx]['vin']:
            if vin['txid'] in mptxs_own_vouts:
                vout = locate_vout(mptxs_own_vouts[vin['txid']], vin['vout'])
                if ismine(vout, address):
                    mptxs_own_vins[mptx] = mptxs[mptx]
                    break
            elif vin['txid'] in txs:
                for vout in txs[vin['txid']]['vout']:
                    if vout['n'] == vin['vout'] and ismine(vout, address):
                        mptxs_own_vins[mptx] = mptxs[mptx]
                        break
                else:
                    break

    #combine filtered mempool and addrindex records
    txs = dict(list(mptxs_own_vouts.items()) + list(mptxs_own_vins.items()) + list(txs.items()))

    for txid in txs:
        tx = txs[txid]
        vouts = [vout for vout in tx['vout'] if ismine(vout, address)]
        for vout in vouts:
            if tx['confirmations']:
                totalReceived += decimal.Decimal(repr(vout['value']))
            else:
                unconfirmedBalance += decimal.Decimal(repr(vout['value']))
        for vin in tx['vin']:
            if 'txid' not in vin or vin['txid'] not in txs:
                continue
            vout = locate_vout(txs[vin['txid']]['vout'], vin['vout'])
            if vout and ismine(vout, address):
                if tx['confirmations']:
                    totalSent += decimal.Decimal(repr(vout['value']))
                else:
                    unconfirmedBalance -= decimal.Decimal(repr(vout['value']))
        if tx['confirmations']:
            txApperances += 1
        else:
            unconfirmedTxApperances += 1
    balance = totalReceived - totalSent
    return {'addrStr': address,
            'balance': float(balance),
            'balanceSat': int(balance * 100000000),
            'totalReceived': float(totalReceived),
            'totalReceivedSat': int(totalReceived * 100000000),
            'totalSent': float(totalSent),
            'totalSentSat': int(totalSent * 100000000),
            'unconfirmedBalance': float(unconfirmedBalance),
            'unconfirmedBalanceSat': int(unconfirmedBalance * 100000000),
            'unconfirmedTxApperances': unconfirmedTxApperances,
            'txApperances': txApperances,
            'transactions': list(txs.keys())}

# Unlike blockexplorers, does not provide 'spent' information on spent vouts.
# This information is not used in clearblockd/clearinghoused anyway.
def gettransaction(tx_hash):
    return lib.bitcoin.rpc('getrawtransaction', [tx_hash, 1])
