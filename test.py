

from coinbase.wallet.client import Client
api_key = 'bMX4e4Jwtpae3kH6'
api_secret = 'Q005dyJjhNU6oYQh9Ut0zbCDwWKzjYhY'
client = Client(api_key, api_secret)
account_id='71c2f280-db2c-583e-89c2-d314915f19d0'
#print client.get_addresses(account_id)
#client.create_address(account_id)
#print client.get_addresses(account_id)
address_id = '1FT1JVmCgqX7MHv6HsTuknhwu9C3EkV3ms'
#print client.get_address_transactions(account_id, address_id)
#client.create_address(account_id,name="hi#123123")
print client.get_addresses(account_id)
#list(filter(lambda x:x.name=="hi#123123",alist.data))

txs = client.get_address_transactions(account_id,address_id)
txs = client.get_transactions(account_id)

tx = client.request_money(account_id,
                           to='nar789@naver.com',
                           amount='1',
                           currency='BTC')