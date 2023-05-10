import aiohttp
import asyncio

import pandas as pd

from datetime import datetime


async def get_url(session, url):

    async with session.get(
            url = url,
            verify_ssl = False
        ) as _response:

        response = await _response.json()
        return response


class Satellite:

    def __init__(self, config):
        self.response = {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "satellite",
                "timestamp": datetime.now(),
                "response": {
                        "counts": {},
                    },
            }
        self.runtime_data = {
                "maindb": f"""http://{config.invs_endpoint}/maindb/hosts?top=15000""",
                "satellite": f"""http://{config.invs_endpoint}/satellite/hosts?per_page=15000""",
                "responses": []
            }

    async def get_data(self):

        async with aiohttp.ClientSession() as session:

            tasks = []

            for src in [ "maindb", "satellite" ]:

                url = self.runtime_data[src]
                tasks.append(asyncio.ensure_future(get_url(session, url)))

            original_responses = await asyncio.gather(*tasks)
            for _response in original_responses:
                self.runtime_data['responses'].append(_response)

    def reconcile(self):

        for _response in self.runtime_data['responses']:

            if _response['module_name'] == "maindb":
                self.runtime_data['dataframe_maindb'] = pd.DataFrame.from_dict( _response['response'] )
            if _response['module_name'] == "satellite":
                self.runtime_data['dataframe_satellite'] = pd.DataFrame.from_dict( _response['response'] )

        self.runtime_data['dataframe_maindb'].drop(
                columns=["ADMIN_WORKGROUP", "CRITICAL"]
            )
        self.runtime_data['dataframe_maindb']['shortname'] = self.runtime_data['dataframe_maindb']['NAME'].str.lower()
        self.runtime_data['dataframe_maindb']['shortname'] = self.runtime_data['dataframe_maindb']['shortname'].str.split(".").str[0]

        self.runtime_data['dataframe_satellite']['shortname'] = self.runtime_data['dataframe_satellite']['name'].str.lower()
        self.runtime_data['dataframe_satellite']['shortname'] = self.runtime_data['dataframe_satellite']['shortname'].str.split(".").str[0]

        _duplicated = self.runtime_data['dataframe_satellite'].loc[
                self.runtime_data['dataframe_satellite'].duplicated(subset=["shortname"]), :]

        self.response['response']['duplicated_at_satellite_ids'] = _duplicated['id'].astype(int).values.tolist()
        self.response['response']['duplicated_at_satellite_names'] = _duplicated['name'].values.tolist()
        self.response['response']['counts']['duplicated_at_satellite'] = _duplicated['id'].count().item()

        _reconciled = pd.merge(
            self.runtime_data['dataframe_maindb'],
            self.runtime_data['dataframe_satellite'],
            how="outer", on="shortname", indicator=True
        )

        _remove_at_satellite = _reconciled.loc[
            _reconciled['_merge'] == "right_only" ]
        self.response['response']['remove_at_satellite_ids'] = _remove_at_satellite['id'].astype(int).values.tolist()
        self.response['response']['remove_at_satellite_names'] = _remove_at_satellite['name'].values.tolist()
        self.response['response']['counts']['remove_at_satellite'] = _remove_at_satellite['id'].count().item()

        _missing_at_satellite = _reconciled.loc[
            _reconciled['_merge'] == "left_only" ]
        self.response['response']['missing_at_satellite_IDs'] = _missing_at_satellite['ID'].astype(int).values.tolist()
        self.response['response']['missing_at_satellite_NAMEs'] = _missing_at_satellite['NAME'].values.tolist()
        self.response['response']['counts']['missing_at_satellite'] = _missing_at_satellite['ID'].count().item()

        return self.response


class OpenManage:

    def __init__(self, config):
        self.response = {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "openmanage",
                "timestamp": datetime.now(),
                "response": {
                        "counts": {},
                    },
            }
        self.runtime_data = {
                "maindb": f"""http://{config.invs_endpoint}/maindb/hosts?top=15000""",
                "openmanage": f"""http://{config.invs_endpoint}/openmanage/hosts?top=1500""",
                "responses": []
            }

    async def get_data(self):

        async with aiohttp.ClientSession() as session:

            tasks = []

            for src in [ "maindb", "openmanage" ]:

                url = self.runtime_data[src]
                tasks.append(asyncio.ensure_future(get_url(session, url)))

            original_responses = await asyncio.gather(*tasks)
            for _response in original_responses:
                self.runtime_data['responses'].append(_response)

    def reconcile(self):

        for _response in self.runtime_data['responses']:

            if _response['module_name'] == "maindb":
                self.runtime_data['dataframe_maindb'] = pd.DataFrame.from_dict( _response['response'] )
            if _response['module_name'] == "openmanage":
                self.runtime_data['dataframe_openmanage'] = pd.DataFrame.from_dict( _response['response'] )

        self.runtime_data['dataframe_maindb'].drop(
                columns=["ADMIN_WORKGROUP", "CRITICAL"]
            )
        self.runtime_data['dataframe_maindb'] = self.runtime_data['dataframe_maindb'].loc[
                self.runtime_data['dataframe_maindb']["SERIALNUMBER"].str.len() == 7 ]
        self.runtime_data['dataframe_maindb'].rename(
                columns={"SERIALNUMBER": "Identifier"}, inplace=True )

        _duplicated = self.runtime_data['dataframe_openmanage'].loc[
                self.runtime_data['dataframe_openmanage'].duplicated(subset=["Identifier"]), :]

        self.response['response']['duplicated_at_openmanage_ids'] = _duplicated['Id'].astype(int).values.tolist()
        self.response['response']['duplicated_at_openmanage_identifiers'] = _duplicated['Identifier'].values.tolist()
        self.response['response']['counts']['duplicated_at_openmanage'] = _duplicated['Id'].count().item()

        _reconciled = pd.merge(
            self.runtime_data['dataframe_maindb'],
            self.runtime_data['dataframe_openmanage'],
            how="outer", on="Identifier", indicator=True
        )

        _remove_at_openmanage = _reconciled.loc[
            _reconciled['_merge'] == "right_only" ]
        self.response['response']['remove_at_openmanage_ids'] = _remove_at_openmanage['Id'].astype(int).values.tolist()
        self.response['response']['remove_at_openmanage_identifiers'] = _remove_at_openmanage['Identifier'].values.tolist()
        self.response['response']['counts']['remove_at_openmanage'] = _remove_at_openmanage['Id'].count().item()

        _missing_at_openmanage = _reconciled.loc[
            _reconciled['_merge'] == "left_only" ]
        self.response['response']['missing_at_openmanage_IDs'] = _missing_at_openmanage['ID'].astype(int).values.tolist()
        self.response['response']['missing_at_openmanage_NAMEs'] = _missing_at_openmanage['NAME'].values.tolist()
        self.response['response']['counts']['missing_at_openmanage'] = _missing_at_openmanage['ID'].count().item()

        return self.response


class AmplifierPack:

    def __init__(self, config):
        self.response = {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "amplifierpack",
                "timestamp": datetime.now(),
                "response": {
                        "counts": {},
                    },
            }
        self.runtime_data = {
                "maindb": f"""http://{config.invs_endpoint}/maindb/hosts?top=15000""",
                "amplifierpack": f"""http://{config.invs_endpoint}/amplifierpack/hosts?top=1500""",
                "responses": []
            }

    async def get_data(self):

        async with aiohttp.ClientSession() as session:

            tasks = []

            for src in [ "maindb", "amplifierpack" ]:

                url = self.runtime_data[src]
                tasks.append(asyncio.ensure_future(get_url(session, url)))

            original_responses = await asyncio.gather(*tasks)
            for _response in original_responses:
                self.runtime_data['responses'].append(_response)

    def reconcile(self):

        for _response in self.runtime_data['responses']:

            if _response['module_name'] == "maindb":
                self.runtime_data['dataframe_maindb'] = pd.DataFrame.from_dict( _response['response'] )
            if _response['module_name'] == "amplifierpack":
                self.runtime_data['dataframe_amplifierpack'] = pd.DataFrame.from_dict( _response['response'] )

        self.runtime_data['dataframe_maindb'].drop(
                columns=["ADMIN_WORKGROUP", "CRITICAL"]
            )
        self.runtime_data['dataframe_maindb'] = self.runtime_data['dataframe_maindb'].loc[
                self.runtime_data['dataframe_maindb']["SERIALNUMBER"].str.len() == 10 ]
        self.runtime_data['dataframe_maindb'].rename(
                columns={"SERIALNUMBER": "SERIALNUMBER"}, inplace=True )

        _duplicated = self.runtime_data['dataframe_amplifierpack'].loc[
                self.runtime_data['dataframe_amplifierpack'].duplicated(subset=["SERIALNUMBER"]), :]

        self.response['response']['duplicated_at_amplifierpack_ids'] = _duplicated['Id'].astype(int).values.tolist()
        self.response['response']['duplicated_at_amplifierpack_serials'] = _duplicated['SERIALNUMBER'].values.tolist()
        self.response['response']['counts']['duplicated_at_amplifierpack'] = _duplicated['Id'].count().item()

        _reconciled = pd.merge(
            self.runtime_data['dataframe_maindb'],
            self.runtime_data['dataframe_amplifierpack'],
            how="outer", on="SERIALNUMBER", indicator=True
        )

        _remove_at_amplifierpack = _reconciled.loc[
            _reconciled['_merge'] == "right_only" ]
        self.response['response']['remove_at_amplifierpack_ids'] = _remove_at_amplifierpack['Id'].astype(int).values.tolist()
        self.response['response']['remove_at_amplifierpack_serials'] = _remove_at_amplifierpack['SERIALNUMBER'].values.tolist()
        self.response['response']['counts']['remove_at_amplifierpack'] = _remove_at_amplifierpack['Id'].count().item()

        _missing_at_amplifierpack = _reconciled.loc[
            _reconciled['_merge'] == "left_only" ]
        self.response['response']['missing_at_amplifierpack_IDs'] = _missing_at_amplifierpack['ID'].astype(int).values.tolist()
        self.response['response']['missing_at_amplifierpack_NAME'] = _missing_at_amplifierpack['NAME'].values.tolist()
        self.response['response']['counts']['missing_at_amplifierpack'] = _missing_at_amplifierpack['ID'].count().item()

        return self.response


class FusionDirector:

    def __init__(self, config):
        self.response = {
                "app_name": config.app_name,
                "service_name": config.service_name,
                "module_name": "fusiondirector",
                "timestamp": datetime.now(),
                "response": {
                        "counts": {},
                    },
            }
        self.runtime_data = {
                "maindb": f"""http://{config.invs_endpoint}/maindb/hosts?top=15000""",
                "fusiondirector": f"""http://{config.invs_endpoint}/fusiondirector/hosts?top=2000""",
                "responses": []
            }

    async def get_data(self):

        async with aiohttp.ClientSession() as session:

            tasks = []

            for src in [ "maindb", "fusiondirector" ]:

                url = self.runtime_data[src]
                tasks.append(asyncio.ensure_future(get_url(session, url)))

            original_responses = await asyncio.gather(*tasks)
            for _response in original_responses:
                self.runtime_data['responses'].append(_response)

    def reconcile(self):

        for _response in self.runtime_data['responses']:

            if _response['module_name'] == "maindb":
                self.runtime_data['dataframe_maindb'] = pd.DataFrame.from_dict( _response['response'] )
            if _response['module_name'] == "fusiondirector":
                self.runtime_data['dataframe_fusiondirector'] = pd.DataFrame.from_dict( _response['response'] )

        self.runtime_data['dataframe_maindb'].drop(
                columns=["ADMIN_WORKGROUP", "CRITICAL"]
            )
        self.runtime_data['dataframe_maindb'] = self.runtime_data['dataframe_maindb'].loc[
                self.runtime_data['dataframe_maindb']["SERIALNUMBER"].str.len() == 20 ]
        self.runtime_data['dataframe_maindb'].rename(
                columns={"SERIALNUMBER": "SERIALNUMBERber"}, inplace=True )

        _duplicated = self.runtime_data['dataframe_fusiondirector'].loc[
                self.runtime_data['dataframe_fusiondirector'].duplicated(subset=["SERIALNUMBERber"]), :]

        self.response['response']['duplicated_at_fusiondirector_ids'] = _duplicated['DeviceID'].values.tolist()
        self.response['response']['duplicated_at_fusiondirector_serials'] = _duplicated['SERIALNUMBERber'].values.tolist()
        self.response['response']['counts']['duplicated_at_fusiondirector'] = _duplicated['DeviceID'].count().item()

        _reconciled = pd.merge(
            self.runtime_data['dataframe_maindb'],
            self.runtime_data['dataframe_fusiondirector'],
            how="outer", on="SERIALNUMBERber", indicator=True
        )

        _remove_at_fusiondirector = _reconciled.loc[
            _reconciled['_merge'] == "right_only" ]
        self.response['response']['remove_at_fusiondirector_ids'] = _remove_at_fusiondirector['DeviceID'].values.tolist()
        self.response['response']['remove_at_fusiondirector_serials'] = _remove_at_fusiondirector['SERIALNUMBERber'].values.tolist()
        self.response['response']['counts']['remove_at_fusiondirector'] = _remove_at_fusiondirector['DeviceID'].count().item()

        _missing_at_fusiondirector = _reconciled.loc[
            _reconciled['_merge'] == "left_only" ]
        self.response['response']['missing_at_fusiondirector_IDs'] = _missing_at_fusiondirector['ID'].astype(int).values.tolist()
        self.response['response']['missing_at_fusiondirector_NAMEs'] = _missing_at_fusiondirector['NAME'].values.tolist()
        self.response['response']['counts']['missing_at_fusiondirector'] = _missing_at_fusiondirector['ID'].count().item()

        return self.response
