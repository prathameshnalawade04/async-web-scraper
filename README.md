# 🕷️ High-Performance Async Web Scraper

![Python](https://img.shields.io/badge/Python-3.9%2B-blue) ![AsyncIO](https://img.shields.io/badge/AsyncIO-Enabled-green) ![Aiohttp](https://img.shields.io/badge/aiohttp-Client-red)

A robust, concurrent web scraper built with **Python 3.10+** and **AsyncIO**. 

This tool demonstrates the power of asynchronous programming by fetching multiple websites in parallel and offloading CPU-intensive parsing to background threads. It achieves significantly higher throughput than traditional synchronous scrapers.

---

## 🚀 Key Features

* **True Concurrency:** Uses `asyncio.gather` to fetch multiple URLs simultaneously, reducing total execution time to the duration of the single slowest request.
* **Non-Blocking Parsing:** Implements `asyncio.to_thread` to run `BeautifulSoup` parsing in a separate thread pool, preventing the Event Loop from freezing during heavy CPU operations.
* **Resource Efficiency:** Utilizes a shared `aiohttp.ClientSession` to reuse TCP connections (Connection Pooling), reducing handshake overhead.
* **Error Handling:** Robust `try/except` blocks to handle network timeouts and bad URLs without crashing the entire batch.

---

## 🛠️ Tech Stack

* **Python:** Core logic and Event Loop management.
* **aiohttp:** Asynchronous HTTP client for non-blocking network requests.
* **BeautifulSoup4:** HTML parsing and data extraction.
* **AsyncIO:** Standard library for concurrent code execution.

---

## 📦 Installation

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/async-web-scraper.git](https://github.com/YOUR_USERNAME/async-web-scraper.git)
    cd async-web-scraper
    ```

2.  **Create a Virtual Environment (Optional but Recommended)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 💻 Usage

1.  Run the main script:
    ```bash
    python main.py
    ```

2.  Follow the interactive prompts to enter the URLs you want to scrape:
    ```text
    Enter 3 URLs (e.g., [https://example.com](https://example.com))
    URL 1: [https://www.python.org](https://www.python.org)
    URL 2: [https://example.com](https://example.com)
    URL 3: [https://www.wikipedia.org](https://www.wikipedia.org)
    ```

3.  **View Results:** The script will output the Title, H1 Headers, and execution time for each site as they finish.

---

## 🧠 How It Works (Architecture)

This project solves the **"Blocking Problem"** typical in web scraping:

1.  **The I/O Bound Task (Network):** We use `async def` and `await` with `aiohttp`. While the program waits for a server to respond, it pauses execution *of that specific task* and switches to the next URL immediately. This is why 3 sites take ~4 seconds total, not 12 seconds.

2.  **The CPU Bound Task (Parsing):**
    Parsing HTML is computationally expensive. If we ran `soup = BeautifulSoup(...)` in the main async loop, it would block the heartbeat of the application. 
    * **Solution:** We wrap the parsing logic in a standard synchronous function (`parse_html`) and send it to a separate thread using `asyncio.to_thread`.
    * **Result:** The Event Loop stays free to manage network packets while the background thread handles the heavy text processing.

### Performance Comparison

| Type | Strategy | Estimated Time (3 Sites) |
| :--- | :--- | :--- |
| **Sync** (`requests`) | Sequential (Wait A, then B, then C) | ~15 Seconds |
| **Async** (This Repo) | Concurrent (Start A, B, C together) | **~5 Seconds** |

---

## 📂 Project Structure

```text
async-web-scraper/
├── main.py              # Entry point and core async logic
├── requirements.txt     # List of dependencies
├── .gitignore           # Files to exclude from Git
└── README.md            # Documentation