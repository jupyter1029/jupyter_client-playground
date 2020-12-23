import pytest
import sys
import asyncio


@pytest.fixture
def event_loop():
    """Local override of pytest-asyncio's event_loop fixture to patch the
    event loop policy on Windows Python >= 3.8.
    """
    if sys.platform.startswith("win") and sys.version_info >= (3, 8):
        try:
            from asyncio import (
                WindowsProactorEventLoopPolicy,
                WindowsSelectorEventLoopPolicy,
            )
        except ImportError:
            pass
            # not affected
        else:
            if type(asyncio.get_event_loop_policy()) is WindowsProactorEventLoopPolicy:
                # WindowsProactorEventLoopPolicy is not compatible with pyzmq
                # fallback to the pre-3.8 default of Selector
                asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()