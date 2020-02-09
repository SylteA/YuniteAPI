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
    await client.add_token(guild_id=123456789, api_key='Your api-key')  # Example token
    

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

For more documentation please view the <a href="https://github.com/SylteA/YuniteAPI/blob/master/DOCUMENTATION.md">documentation</a>

Want to support me? <a href="https://www.patreon.com/bePatron?u=22098744" data-patreon-widget-type="become-patron-button">Become a Patron!</a><script async src="https://c6.patreon.com/becomePatronButton.bundle.js"></script>
