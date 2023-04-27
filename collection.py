# class Collection:
#     def __init__(self, name, address, assetCount, change24, reward_points, floor_price):
#         self.name = name
#         self.address = address
#         self.assetCount = assetCount
#         self.change24 = change24
#         self.reward_points = reward_points
#         self.floor_price = floor_price
from body1 import body1
import requests
import json

class Collection:
    def __init__(self, name, address, assetCount, change24, reward_points, floor_price):
        self.name = name
        self.address = address
        self.assetCount = assetCount
        self.change24 = change24
        self.reward_points = reward_points
        self.floor_price = floor_price

    @classmethod
    def get_collections(cls):
        resp = requests.post(url="https://api.minted.network/graphql", json=body1)
        lin = resp.json()
        collections = []
        nft_addresses = []
        for nft in lin['data']['collections']['edges']:
            name = nft['node']['name']
            address = nft['node']['address']
            asset_count = nft['node']['assetCount']
            if nft['node']['floorPrice']['change24h'] is not None:
                change24 = float(nft['node']['floorPrice']['change24h'])
                change24 = round(change24, 1)
            else:
                change24 = 0
            reward_points = nft['node']['rewardPoints']
            if nft['node']['floorPrice']['latestFloorPriceNative'] is not None:
                floor_price = int(nft['node']['floorPrice']['latestFloorPriceNative']) / 1000000000000000000
            else:
                floor_price = 0
            collection = cls(name, address, asset_count, change24, reward_points, floor_price)
            collections.append(collection)
            nft_address = {'name': collection.name, 'address': collection.address}
            nft_addresses.append(nft_address)
        with open('collection_addresses2.json', 'w') as f:
            json.dump(nft_addresses, f)
        return collections
