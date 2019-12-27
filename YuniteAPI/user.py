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

class YUser(object):
    """The User object returned from API
    Mostly a placeholder, methods may come in the future"""
    def __init__(self, *,
                 discordID: int,
                 epicID: str,
                 epicDisplayName: str,
                 inputMethod: str,
                 platform: str
                 ):
        self.user_id = discordID
        self.epic_id = epicID
        self.displayname = epicDisplayName
        self.input_method = inputMethod
        self.platform = platform

    def __repr__(self):
        return '<YuniteUser user_id={0.user_id} epic_id={0.epic_id} displayname={0.displayname} ' \
               'input_method={0.input_method} platform={0.platform}>'.format(self)
