import aiosqlite
import asyncio
import aiohttp
from bs4 import BeautifulSoup

def parsing(html):
    soup=BeautifulSoup(html,'html.parser')
    title=soup.title.string if soup.title else "unknown_page"
    h1_tags=[h.get_text().strip() for h in soup.find_all('h1')]
    h2_tags=[h.get_text() for h in soup.find_all('h2')]
    h1=','.join(h1_tags)
    h2=','.join(h2_tags)
    return (title,h1,h2)

async def scraping(session,urls,db):
    l=tuple()
    async with session.get(urls) as response:
        html=await response.text()
        result=await asyncio.to_thread(parsing,html)
        await db.execute("insert into scraped values(?,?,?)",(result))
        await db.commit()
    print("your data is now avilabe in the database!")

async def main():
    urls = []
    # Collect inputs first
    print("Enter 3 URLs (e.g., https://example.com)")
    for x in range(3):
        u = input(f"URL {x+1}: ").strip()
        urls.append(u)

    print("\n🚀 Starting Concurrent Scrape...")
    
    async with aiosqlite.connect("scraped") as db:
        await db.execute("create table if not exists scraped(title text ,h1_tag text,h2_tag text )")
        await db.commit()
        print("the scraped database is used to store the data!")
        async with aiohttp.ClientSession() as session:
            tasks=[]
            for x in urls:
                tasks.append(scraping(session,x,db))

            await asyncio.gather(*tasks)

        print("\n📊 --- FINAL DATABASE CONTENT ---")
        async with db.execute("SELECT * FROM scraped ORDER BY title") as cursor:
            rows = await cursor.fetchall()  
            for row in rows:
                print(f"Title: {row[0]}")
                print(f"H1s:   {row[1][:50]}...")
                print(f"H2s:   {row[2][:50]}...") 
                print("-" * 20)

if __name__=='__main__':
    asyncio.run(main())
