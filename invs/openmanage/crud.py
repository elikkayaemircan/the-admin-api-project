import aiohttp
import asyncio

from datetime import datetime


async def get_url(config, session, url):

    async with session.get(
            url = url,
            auth = aiohttp.BasicAuth(config.idrac_user, config.idrac_pass),
            verify_ssl = False
        ) as _response:

        response = await _response.json()
        return response


async def get_hosts(config, skip, top):

    response = []

    async with aiohttp.ClientSession() as session:

        tasks = []

        url = f"""https://{config.idrac_host}/api/DeviceService/Devices?$skip={skip}&$top={top}"""
        tasks.append(asyncio.ensure_future(get_url(config, session, url)))

        original_responses = await asyncio.gather(*tasks)
        for _response in original_responses:
            response = response + _response['value']

        if response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "openmanage",
                "timestamp": datetime.now(),
                "response": response,
            }

        return None


async def get_w_id(config, id: int):

    async with aiohttp.ClientSession() as session:

        url = f"""https://{config.idrac_host}/api/DeviceService/Devices({id})"""
        response = await get_url(config, session, url)

        if "error" not in response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "openmanage",
                "timestamp": datetime.now(),
                "response": [ response ],
            }

        return None
