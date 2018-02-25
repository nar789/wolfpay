from coinbase.wallet.client import Client


def create_address(sid,pid):
	api_key = 'bMX4e4Jwtpae3kH6'
	api_secret = 'Q005dyJjhNU6oYQh9Ut0zbCDwWKzjYhY'
	client = Client(api_key, api_secret)
	name="%s#%s" % (sid,pid)
	addr=client.create_address(account_id,name=name)
	return addr