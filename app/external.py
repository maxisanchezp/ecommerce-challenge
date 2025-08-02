import httpx

EXTERNAL_API_BASE = 'https://fakestoreapi.com' #MOCK

async def get_external_product(product_id: int) -> dict:
    
    ## Llama a una API externa, se usa fakestoreapi como mock
    
    url = f"{EXTERNAL_API_BASE}/products/{product_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()