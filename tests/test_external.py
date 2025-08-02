import pytest
import asyncio

from app.external import get_external_product

@pytest.mark.asyncio
async def test_get_external_product():
    data = await get_external_product(1)
    assert "id" in data
    assert data['id'] == 1