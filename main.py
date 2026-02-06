import aiohttp as io
import asyncio
import time
from bs4 import BeautifulSoup

# --- PART 1: The Worker (Blocking CPU code) ---
def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.title.string if soup.title else "No Title"
    # Get text of all H1s cleanly
    h1_list = [h.get_text().strip() for h in soup.find_all('h1')]
    return title, h1_list

# --- PART 2: The Manager (Async I/O code) ---
async def scrapping(url, session):
    start_time = time.time()
    print(f"🔄 Fetching: {url}...")
    
    try:
        async with session.get(url) as response:
            html = await response.text()
            
            title, headers = await asyncio.to_thread(parse_html, html)
            
            # Print Results
            print(f"\n✅ FINISHED: {url}")
            print(f"   Title: {title}")
            print(f"   H1 Tags: {headers}")
            
            end_time = time.time()
            print(f"   ⏱️ Time taken: {end_time - start_time:.2f}s")
            
    except Exception as e:
        print(f"❌ Error with {url}: {e}")

async def main():
    urls = []
    # Collect inputs first
    print("Enter 3 URLs (e.g., https://example.com)")
    for x in range(3):
        u = input(f"URL {x+1}: ").strip()
        urls.append(u)

    print("\n🚀 Starting Concurrent Scrape...")
    
    async with io.ClientSession() as session:
        tasks = []
        for url in urls:
            # Create task with the shared session
            tasks.append(scrapping(url, session))
        
        # Run all at once
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())