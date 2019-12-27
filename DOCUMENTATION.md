<h1>YuniteAPI</h1>

A asynchronous wrapper for the Yunite API

<h1>Getting Started:</h1>
Install the package using one of the following commands:
<li> <strong> pip install YuniteAPI </strong> </li>
<li> <strong> pip install -U YuniteAPI </strong> </li>
<li> <strong> python -m pip install -U git+https://github.com/SylteA/YuniteAPI.git </strong> </li>
<hr>

After that, create the client using the following code:
```python
import YuniteAPI
import asyncio


async def main():
    client = YuniteAPI.Client()
    await client.add_token(guild_id=123123, api_key='Your api-key') # Add a api-key for that guild_id
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```
<hr>
For future reference in this documentation: when referring to 'client' we refer to what has been defined above!

<h3>Using the wrapper</h3>
<hr>
<strong>await client.fetch_user(guild_id=123456789, user_id=123456789)</strong>

Fetch a single user id by discord or epic id

<strong>await client.fetch_users(guild_id=123456789, user_ids=[123456789, 123456789])</strong>

Fetch users in bulk by discord or epic id
