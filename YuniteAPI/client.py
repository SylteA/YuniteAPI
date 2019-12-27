"""
MIT License

Copyright (c) 2019 Sylte

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from .exceptions import (
    PaymentRequired, Forbidden, TooManyRequests, InvalidInput,
    UnexpectedResponse, InvalidEndpoint, Unauthorized, YuniteAPIError
        )
from .user import YUser

from typing import Optional, Union, List
import asyncio
import aiohttp
import json


class Client:
    """The YuniteAPI Client class"""
    def __init__(self,
                 loop: Optional[asyncio.AbstractEventLoop] = None,
                 session: Optional[aiohttp.ClientSession] = None,
                 **session_kwargs):

        if 'headers' in session_kwargs:
            del session_kwargs['headers']

        self.session: Optional[aiohttp.ClientSession] = session
        self.loop: Optional[asyncio.AbstractEventLoop] = loop

        self._ready = asyncio.Event(loop=loop)

        self._api_tokens = {}

        self._base_url = "https://yunite.xyz/api/v2/servers/"
        self.__session_kwargs = session_kwargs
        self._setup()

    def _url_for(self,
                 guild_id: int, *,
                 multiple: bool = False,
                 by: str = "byDiscordID") -> str:
        """
        Return a cleaned up endpoint url

        :param guild_id[int]:
            The guild id you want to fetch from
        :param multiple[bool]:
            Url to fetch multiple or one user(s)
        :param by[str]:
            Fething by Epic id or Discord id:
            Possible values:
                - byDiscordID
                - byEpicID

        :returns:
            A properly formatted API endpoint.
            endpoints may change in the future

        :raises:
            :exc: `YuniteAPI.InvalidEndpoint`
                param `by` received wrong input
        """
        if by is None:
            by = "byDiscordID"

        if by not in ('byDiscordID', 'byEpicID'):
            raise InvalidEndpoint(f'Recieved input `{by}`, expected `byDiscordID` or `byEpicID`') from None

        multiple = 'bulk' if multiple else 'single'
        return f'{self._base_url}{guild_id}/regsys/{multiple}/{by}'

    async def _ensure_session(self) -> None:
        """Assure that there is a ClientSession running"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(loop=self.loop, **self.__session_kwargs)

    def _setup(self) -> None:
        """Create the initial ClientSession and set the ready event"""
        if not isinstance(self.loop, asyncio.AbstractEventLoop):
            self.loop = asyncio.get_event_loop()

        if not isinstance(self.session, aiohttp.ClientSession):
            self.loop.create_task(self._ensure_session())

        self._ready.set()

    def is_ready(self) -> bool:
        """Specifies if the clients session is ready for use."""
        return self._ready.is_set()

    @property
    def closed(self) -> bool:
        """Specifies if the clients session is closed"""
        return not self.is_ready()

    async def wait_until_ready(self):
        """Wait until the clients session is ready"""
        await self._ready.wait()

    async def close(self) -> None:
        """Close the running client session and clear the ready event"""
        if self.closed:
            return

        await self.session.close()
        self.session = None
        self._ready.clear()

    @staticmethod
    async def _read_response(response: aiohttp.ClientResponse, *,
                             raise_errors: bool = True) -> dict:
        """
        Read a response and return the json read

        :param response[aiohttp.ClientResponse]:
        :param raise_errors[bool]

        :returns:
            Clean `dict`

        :raises:
            :exc: `YuniteAPI.UnexpectedResponse`
                Could not read the `ClientResponse` as json
        """
        try:
            response_json = await response.json()
        except aiohttp.ContentTypeError:
            response_text = await response.text()
            raise UnexpectedResponse(response=response, response_text=response_text) from None
        else:
            if raise_errors:
                return response_json

    async def _get_errors(self,
                          response: aiohttp.ClientResponse,
                          response_dict: dict,
                          raise_errors: bool = True) -> None:

        if response.status != 200:

            if raise_errors:
                if response.status == 401:
                    if len(self._api_tokens.items()) <= 0:
                        await self.close()
                    raise Unauthorized(f'Provided token is invalid. '
                                       f'Please try again later with a different token.') from None

                elif response.status == 402:
                    raise PaymentRequired(response_dict.get('message',
                                                            'API Access is not available on the free plan')) from None

                elif response.status == 403:
                    raise Forbidden('That API token is not valid for this Guild') from None

                elif response.status == 429:
                    raise TooManyRequests(response_dict.get('message', 'Ratelimit exceeded')) from None

                else:
                    raise UnexpectedResponse(response=response, response_json=response_dict)

    async def _get(self, url: str, guild_id: int,
                   auth_header: dict = None,
                   raise_errors: bool = True) -> dict:
        if not self.is_ready():
            await self.wait_until_ready()

        await self._ensure_session()

        if auth_header is None:
            auth_header = self._api_tokens.get(str(guild_id), None)
            if auth_header is None:
                if len(self._api_tokens.items()) <= 0:
                    await self.close()
                raise InvalidInput(f'Could not find a token for this guild id. '
                                   f'Add it using `YuniteAPI.Client.add_token`') from None
            auth_header = {'Y-Api-Key': auth_header}

        async with self.session.get(url, headers=auth_header) as response:

            response_dict = await self._read_response(response=response, raise_errors=raise_errors)
            await self._get_errors(response, response_dict=response_dict, raise_errors=raise_errors)

            return response_dict

    async def _post(self, url: str, guild_id: int,
                    auth_header: dict = None,
                    raise_errors: bool = True,
                    *, ids: List[int]):
        if not self.is_ready():
            await self.wait_until_ready()

        await self._ensure_session()

        if auth_header is None:
            auth_header = self._api_tokens.get(str(guild_id), None)
            if auth_header is None:
                if len(self._api_tokens.items()) <= 0:
                    await self.close()
                raise InvalidInput(f'Could not find a token for this guild id. '
                                   f'Add it using `YuniteAPI.Client.add_token`') from None
            auth_header = {'Y-Api-Key': auth_header, 'Content-Type': 'application/json'}
        ids = json.dumps([str(id) for id in ids])
        async with self.session.post(url=url, headers=auth_header, data=ids) as response:

            response_dict = await self._read_response(response=response, raise_errors=raise_errors)
            await self._get_errors(response, response_dict=response_dict, raise_errors=raise_errors)

            return response_dict

    async def _check_key(self, key: str, guild_id: int) -> bool:
        url = f'{self._url_for(guild_id=guild_id)}/0'
        auth_header = {'Y-Api-Key': key}
        try:
            await self._get(url=url, guild_id=guild_id, auth_header=auth_header)
        except YuniteAPIError as e:
            await self.close()
            raise InvalidInput(f'Token is invalid: \n{e.message}')
        else:
            return True

    async def add_token(self, *, guild_id: int, api_key: str) -> None:
        try:
            if await self._check_key(guild_id=guild_id, key=api_key):
                self._api_tokens[str(guild_id)] = api_key
        except InvalidInput as e:
            raise e from None

    def __del__(self):
        self.loop.create_task(self.close())

    """ Fetch functions """

    async def fetch_user(self, *, guild_id: int, user_id: int, by: str = None) -> Union[YUser, None]:
        """
        Fetch a single user id by discord or epic id

        :param guild_id:
            The guild to query from
        :param user_id:
            The user to query for
        :param by:
            The type of ID to query from
            Valid types are:
                - byDiscordID (default)
                - byEpicID

        :returns:
            `Union[YuniteAPI.YUser, None]`

        """
        url = f'{self._url_for(guild_id=guild_id, multiple=False, by=by)}/{user_id}'
        user = await self._get(url=url, guild_id=guild_id)
        if user.pop('found'):
            if user.pop('isLinked'):
                return YUser(**user)
        return None

    async def fetch_users(self, *, guild_id: int, by: str = 'byDiscordID',
                          user_ids: List[int]) -> dict:
        """
        Fetch users in bulk by discord or epic id

        :param guild_id:
            The guild to query from
        :param by:
            The type of ID to query from
            Valid types are:
                - byDiscordID (default)
                - byEpicID
        :param user_ids:
            A list of user ids you want to fetch

        :returns:
            dict of ``{"user_id": Union[YuniteAPI.YUser, None]}``
        """
        url = self._url_for(guild_id=guild_id, multiple=True, by=by)
        response = await self._post(url=url, guild_id=guild_id, ids=user_ids)
        return_dict = {}
        for user in response.pop('users'):
            if user.pop('found'):
                if user.pop('isLinked'):
                    if by == 'byDiscordID':
                        return_dict[user['discordID']] = YUser(**user)
                    else:
                        return_dict[user['epicID']] = YUser(**user)

        for user in response.pop('invalidIDs'):
            return_dict[user] = None

        return return_dict
