import aiohttp
import asyncio

from datetime import datetime


async def get_url(config, session, url):

    async with session.get(
            url = url,
            auth = aiohttp.BasicAuth(config.ilo_user, config.ilo_pass),
            verify_ssl = False
        ) as _response:

        response = await _response.json(content_type=None)
        return response


async def get_host_ids(config, skip, top):

    ids = []

    _odata_ids = []

    _top_limit = 500
    _number_of_steps = divmod( top - 1, _top_limit )

    async with aiohttp.ClientSession() as session:

        tasks = []

        if _number_of_steps[0] < 1:

            url = f"""https://{config.ilo_host}/redfish/v1/AggregatorService/ManagedSystems?$skip={skip}"""
            tasks.append(asyncio.ensure_future(get_url(config, session, url)))

        if _number_of_steps[0] >= 1:

            for _step in range(_number_of_steps[0] + 1):
                _skip = skip + ( _top_limit * _step )
                url = f"""https://{config.ilo_host}/redfish/v1/AggregatorService/ManagedSystems?$skip={_skip}"""
                tasks.append(asyncio.ensure_future(get_url(config, session, url)))

        original_responses = await asyncio.gather(*tasks)
        for _response in original_responses:
            if ( "Members" in _response ): _odata_ids.append( _response['Members'] )

        for _id in _odata_ids:
            ids = ids + _id

        return ids


async def get_hosts(config, skip, top):

    response = []

    ids = await get_host_ids(config, skip, top)

    async with aiohttp.ClientSession() as session:

        tasks = []

        for _id in ids[:top]:

            _id = _id['@odata.id'].split('/')[-1]
            url = f"""https://{config.ilo_host}/redfish/v1/Systems/{_id}"""
            tasks.append(asyncio.ensure_future(get_url(config, session, url)))

        original_responses = await asyncio.gather(*tasks)
        for _response in original_responses:
            response.append( _response )

        if response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "amplifierpack",
                "timestamp": datetime.now(),
                "response": response,
            }

        return None


async def get_w_id(config, id: str):

    async with aiohttp.ClientSession() as session:

        url = f"""https://{config.ilo_host}/redfish/v1/Systems/{id}"""
        response = await get_url(config, session, url)

        if "error" not in response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "amplifierpack",
                "timestamp": datetime.now(),
                "response": [ response ],
            }

        return None
