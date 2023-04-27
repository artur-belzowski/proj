body1 = {
        "operationName": "getCollections",
        "variables": {
            "first": 50,
            "filter": {
                "chains": [
                    "CRONOS",
                    # "ETHEREUM"
                ],
                "verifiedOnly": True
            },
            "sort": {
                "field": "VOLUME_ONE_DAY",
                "isAscending": None
            }
        },
        "query": "query getCollections($sort: CollectionSortInput, $filter: CollectionFilterInput, $after: String, $first: Int!) {\n  collections(first: $first, filter: $filter, sort: $sort, after: $after) {\n    edges {\n      node {\n        ...CollectionDetailFields\n        ...CollectionPriceFields\n        ...CollectionVolumeFields\n        rewardPoints\n        __typename\n      }\n      cursor\n      __typename\n    }\n    pageInfo {\n      ...PageInfoFields\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment CollectionDetailFields on AssetCollection {\n  ...CollectionIdentifyFields\n  name\n  logo {\n    url\n    __typename\n  }\n  banner {\n    url\n    __typename\n  }\n  creator {\n    ...UserFields\n    __typename\n  }\n  description\n  assetCount\n  ownerCount\n  raritySource\n  isRarityEnable\n  isCollectionOfferEnable\n  highestCollectionOffer\n  __typename\n}\n\nfragment CollectionIdentifyFields on AssetCollection {\n  address\n  name\n  chain {\n    name\n    __typename\n  }\n  status\n  __typename\n}\n\nfragment UserFields on UserAccount {\n  evmAddress\n  name\n  avatar {\n    url\n    __typename\n  }\n  nonce\n  __typename\n}\n\nfragment CollectionPriceFields on AssetCollection {\n  floorPrice {\n    change24h\n    latestFloorPrice\n    latestFloorPriceNative\n    globalFloorPrice7dNative\n    globalFloorPrice24hNative\n    globalFloorPrice30dNative\n    globalFloorPriceAllNative\n    __typename\n  }\n  __typename\n}\n\nfragment CollectionVolumeFields on AssetCollection {\n  volume {\n    change24h\n    volume7d\n    volume24h\n    volume30d\n    volumeAll\n    globalVolume7dNative\n    globalVolume24hNative\n    globalVolume30dNative\n    globalVolumeAllNative\n    __typename\n  }\n  __typename\n}\n\nfragment PageInfoFields on PageInfo {\n  hasPreviousPage\n  hasNextPage\n  startCursor\n  endCursor\n  __typename\n}"
    }