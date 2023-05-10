import aiohttp
import asyncio

from datetime import datetime


async def get_url(config, session, url):

    async with session.get(
            url = url,
            auth = aiohttp.BasicAuth(config.satellite_user, config.satellite_pass),
            verify_ssl = False
        ) as _response:

        response = await _response.json()
        return response


async def get_hosts(config, per_page, page):

    response = []

    async with aiohttp.ClientSession() as session:

        tasks = []

        url = f"""https://{config.satellite_host}/api/v2/hosts?thin=true&per_page={per_page}&;page={page}"""
        tasks.append(asyncio.ensure_future(get_url(config, session, url)))

        original_responses = await asyncio.gather(*tasks)
        for _response in original_responses:
            response = response + _response['results']

        if response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "satellite",
                "timestamp": datetime.now(),
                "response": response,
            }

        return None


async def get_w_id(config, id):

    async with aiohttp.ClientSession() as session:

        url = f"""https://{config.satellite_host}/api/v2/hosts/{id}"""
        response = await get_url(config, session, url)

        if "error" not in response:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "satellite",
                "timestamp": datetime.now(),
                "response": [ response ],
            }

        return None


async def get_w_name(config, name):

    async with aiohttp.ClientSession() as session:

        url = f"""https://{config.satellite_host}/api/v2/hosts?search={name}"""
        response = await get_url(config, session, url)

        if response['subtotal'] == 1:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "satellite",
                "timestamp": datetime.now(),
                "response": response['results'],
            }

        if response['subtotal'] > 1:

            return {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "satellite",
                "timestamp": datetime.now(),
                "response": [ { "id": element['id'], "name": element['name'] }  for element in response['results'] ],
            }

        return None
