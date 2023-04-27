import json
import requests

def get_nft_data(collection_name):
    with open('collection_addresses2.json', 'r') as f:
        collections = json.load(f)

    selected_collection = next((c for c in collections if c['name'] == collection_name), None)
    if selected_collection is None:
        return 'Nie znaleziono kolekcji o nazwie {}'.format(collection_name)

    body2 = {
        "operationName": "getCollectionAssets",
        "variables": {
            "address": selected_collection['address'],
            "chain": "CRONOS",
            "first": 50,
            "filter": {
                "chain": "CRONOS",
                "listingType": None,
                "priceRange": None,
                "attributes": None,
                "rarityRange": None,
                "nameOrTokenId": None
            },
            "sort": "LOWEST_PRICE"
        },
        "query": "query getCollectionAssets($address: EvmAddress!, $chain: Blockchain!, $first: Int!, $sort: AssetSort!, $after: String, $filter: AssetFilterInput) {\n  collection(address: $address, chain: $chain) {\n    ...CollectionIdentifyFields\n    assets(first: $first, after: $after, filter: $filter, sort: $sort) {\n      totalCount\n      edges {\n        node {\n          ...AssetDetailFields\n          bids(first: 1) {\n            edges {\n              node {\n                ...OrderFields\n                __typename\n              }\n              cursor\n              __typename\n            }\n            pageInfo {\n              ...PageInfoFields\n              __typename\n            }\n            totalCount\n            __typename\n          }\n          __typename\n        }\n        cursor\n        __typename\n      }\n      pageInfo {\n        ...PageInfoFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CollectionIdentifyFields on AssetCollection {\n  address\n  name\n  chain {\n    name\n    __typename\n  }\n  status\n  __typename\n}\n\nfragment AssetDetailFields on Asset {\n  name\n  tokenId\n  image {\n    url\n    __typename\n  }\n  animatedImage {\n    url\n    __typename\n  }\n  owner {\n    ...UserFields\n    __typename\n  }\n  ask {\n    ...OrderFields\n    __typename\n  }\n  collection {\n    ...CollectionIdentifyFields\n    __typename\n  }\n  rarityRank\n  __typename\n}\n\nfragment UserFields on UserAccount {\n  evmAddress\n  name\n  avatar {\n    url\n    __typename\n  }\n  nonce\n  __typename\n}\n\nfragment OrderFields on MakerOrder {\n  hash\n  chain\n  isOrderAsk\n  collection\n  tokenId\n  currency\n  strategy\n  startTime\n  endTime\n  minPercentageToAsk\n  nonce\n  price\n  amount\n  status\n  signer\n  encodedParams\n  paramTypes\n  signature\n  __typename\n}\n\nfragment PageInfoFields on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}"
    }

    resp = requests.post(url="https://api.minted.network/graphql", json=body2)
    nft_data = []
    for edge in resp.json()['data']['collection']['assets']['edges']:
        token_id = edge['node']['ask']['tokenId']
        nft_price = int(edge['node']['ask']['price']) / 1000000000000000000
        rarity_rank = edge['node']['rarityRank']
        nft_data.append({'token_id': token_id, 'nft_price': nft_price, 'rarity_rank': rarity_rank})
    return nft_data
