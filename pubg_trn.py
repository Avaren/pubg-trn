import asyncio

import aiohttp

API_ROOT = 'https://pubgtracker.com/api'
API_PROFILE = '{}/profile/{{}}/{{}}'.format(API_ROOT)
API_SEARCH = '{}/search'.format(API_ROOT)


class NotFound(Exception):
    pass


class PUBGTRN:
    def __init__(self, key, session=None, loop=None):
        self.loop = loop or asyncio.get_event_loop()
        self.session = session or aiohttp.ClientSession(loop=self.loop)
        self.headers = {
            'content-type': "application/json",
            'trn-api-key': key,
        }

    async def search(self, id, mode='steamId'):
        async with self.session.get(API_SEARCH, params={mode: id}, headers=self.headers) as req:
            if req.status == 200:
                return await req.json()
            else:
                raise NotFound()

    async def profile(self, name, platform='pc'):
        async with self.session.get(API_PROFILE.format(platform, name), headers=self.headers) as req:
            if req.status == 200:
                return await req.json()
            else:
                raise NotFound()
