import aiohttp
import asyncio

from datetime import datetime


async def get_url(config, session, url):

    async with session.get(
            url = url,
            auth = aiohttp.BasicAuth(config.ibmc_user, config.ibmc_pass),
            verify_ssl = False
        ) as _response:

        response = await _response.json()
        return response


async def get_hosts(config, skip, top):

    response = []

    _top_limit = 500
    _number_of_steps = divmod( top - 1, _top_limit )

    async with aiohttp.ClientSession() as session:

        tasks = []

        if _number_of_steps[0] < 1:

            url = f"""https://{config.ibmc_host}/redfish/v1/rich/Nodes?$skip={skip}&$top={top}"""
            response = await get_url(config, session, url)

            if response:

                return {
                    "app_name": config.app_name,
                    "service_name": config.service_name,
                    "module_name": "fusiondirector",
                    "timestamp": datetime.now(),
                    "response": response['Members'],
                }

        if _number_of_steps[0] >= 1:

            for _step in range(_number_of_steps[0]):
                _skip = skip + ( _top_limit * _step )
                url = f"""https://{config.ibmc_host}/redfish/v1/rich/Nodes?$skip={_skip}&$top={_top_limit}"""
                tasks.append(asyncio.ensure_future(get_url(config, session, url)))

            _skip = _skip + _top_limit
            _top = top - _skip
            url = f"""https://{config.ibmc_host}/redfish/v1/rich/Nodes?$skip={_skip}&$top={_top}"""
            tasks.append(asyncio.ensure_future(get_url(config, session, url)))

            original_responses = await asyncio.gather(*tasks)
            for _response in original_responses:
                response = response + _response['Members']

            if response:

                return {
                    "app_name": config.app_name,
                    "service_name": config.service_name,
                    "module_name": "fusiondirector",
                    "timestamp": datetime.now(),
                    "response": response,
                }

        return None


async def get_w_id(config, id: str):

    async with aiohttp.ClientSession() as session:

        url = f"""https://{config.ibmc_host}/redfish/v1/rich/Nodes/{id}"""
        response = await get_url(config, session, url)

        if "error" not in response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "fusiondirector",
                "timestamp": datetime.now(),
                "response": [ response ],
            }

        return None
