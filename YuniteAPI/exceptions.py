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

from typing import Optional
import aiohttp


class YuniteAPIError(Exception):
    def __init__(self, message: str):
        self.message = message


class Unauthorized(YuniteAPIError):
    """Will be raised if you fail to provide a valid and existing API key."""
    def __init__(self, message: str):
        super().__init__(message=message)


class PaymentRequired(YuniteAPIError):
    """Will be raised if you query a guild that does not have Yunite Premium."""
    def __init__(self, message: str):
        super().__init__(message=message)


class Forbidden(YuniteAPIError):
    """Will be raised if the specified API key is not authorized to access the specified guild."""
    def __init__(self, message: str):
        super().__init__(message=message)


class TooManyRequests(YuniteAPIError):
    """Will be returned if you violate Yunites ratelimits.

    These ratelimits are dynamic, so we want you to NOT HARDCODE them.
    Instead, you should check the header on reach response,
    and adapt your applications behavior accordingly."""
    def __init__(self, message: str):
        super().__init__(message=message)


class InvalidEndpoint(YuniteAPIError):
    """Will be raised if you fail to provide a valid endpoint"""
    def __init__(self,
                 endpoint: str, *,
                 message: str = None):
        self.endpoint = endpoint
        super().__init__(message=message)

    def __repr__(self):
        response = self.message if self.message else self.endpoint
        return '<InvalidEndpoint, endpoint={}>'.format(response)


class InvalidInput(YuniteAPIError):
    """Raised when any input is invalid"""
    def __init__(self, message: str):
        super().__init__(message=message)


class UnexpectedResponse(YuniteAPIError):
    def __init__(self,
                 response: aiohttp.ClientResponse,
                 response_json: Optional[dict] = None,
                 response_text: str = ""):
        self.response = response
        self.status = self.response.status
        self.response_json = response_json or {}
        self.response_text = response_text

        response_safe = str(self.response_json) if self.response_json else self.response_text
        super().__init__(message=response_safe)

    def __repr__(self):
        message = self.response_json if self.response_json else self.response_text
        return '<UnexpectedResponse status={0} response={1}>'.format(self.status, message)
