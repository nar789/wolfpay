from coinbase.wallet.client import Client


def create_address(sid,pid):
	api_key = 'bMX4e4Jwtpae3kH6'
	api_secret = 'Q005dyJjhNU6oYQh9Ut0zbCDwWKzjYhY'
	client = Client(api_key, api_secret)
	account_id='71c2f280-db2c-583e-89c2-d314915f19d0'
	name="%s#%s" % (sid,pid)
	addr=client.create_address(account_id,name=name)
	return addr


def get_transaction(addr):
	api_key = 'bMX4e4Jwtpae3kH6'
	api_secret = 'Q005dyJjhNU6oYQh9Ut0zbCDwWKzjYhY'
	client = Client(api_key, api_secret)
	account_id='71c2f280-db2c-583e-89c2-d314915f19d0'
	txs = client.get_address_transactions(account_id,addr)
	return txs;