import asyncio
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv
from os import getenv, makedirs

load_dotenv()

# Script grabs the OpenAI API Key and error checks for a missing key
OPENAI_API_KEY = getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Please set it in your .env file.")

# List of specific Investopedia URLs to scrape
urls = [
    "https://www.investopedia.com/trading/hedging-beginners-guide/",
    "https://www.investopedia.com/magnificent-seven-stocks-8402262",
    "https://www.investopedia.com/terms/i/incomestock.asp",
    "https://www.investopedia.com/terms/f/fundamentalanalysis.asp",
    "https://www.investopedia.com/terms/p/price-earningsratio.asp",
    "https://www.investopedia.com/terms/s/swot.asp",
    "https://www.investopedia.com/terms/m/metrics.asp",
    "https://www.investopedia.com/terms/m/marketvalue.asp",
    "https://www.investopedia.com/ask/answers/021015/what-best-measure-given-stocks-volatility.asp",
    "https://www.investopedia.com/articles/basics/12/intrinsic-value.asp",
    "https://www.investopedia.com/terms/r/requiredrateofreturn.asp",
    "https://www.investopedia.com/articles/fundamental-analysis/09/free-cash-flow-yield.asp",
    "https://www.investopedia.com/terms/a/assetvaluation.asp",
    "https://www.investopedia.com/terms/s/stockholdersequity.asp",
    "https://www.investopedia.com/ask/answers/070915/how-do-you-calculate-company-equity.asp",
    "https://www.investopedia.com/terms/o/optionscontract.asp",
    "https://www.investopedia.com/terms/d/derivative.asp",
    "https://www.investopedia.com/covered-call-etfs-7975323",
    "https://www.investopedia.com/how-to-trade-options-7378194",
    "https://www.investopedia.com/terms/c/calendarspread.asp",
    "https://www.investopedia.com/articles/optioninvestor/10/derivatives-101.asp",
    "https://www.investopedia.com/articles/active-trading/082113/what-spread-betting.asp",
    "https://www.investopedia.com/terms/s/swaprate.asp",
    "https://www.investopedia.com/ask/answers/050515/it-better-use-fundamental-analysis-technical-analysis-or-quantitative-analysis-evaluate-longterm.asp",
    "https://www.investopedia.com/supertrend-indicator-7976167",
    "https://www.investopedia.com/articles/trading/04/120804.asp",
    "https://www.investopedia.com/articles/active-trading/092315/5-most-powerful-candlestick-patterns.asp",
    "https://www.investopedia.com/trading/candlestick-charting-what-is-it/",
    "https://www.investopedia.com/terms/r/riskmanagement.asp",
    "https://www.investopedia.com/terms/e/enterprise-risk-management.asp",
    "https://www.investopedia.com/articles/active-trading/041814/four-most-commonlyused-indicators-trend-trading.asp",
    "https://www.investopedia.com/articles/trading/06/advcandlesticks.asp",
    "https://www.investopedia.com/terms/r/relativestrength.asp",
    "https://www.investopedia.com/trading/support-and-resistance-basics/",
    "https://www.investopedia.com/terms/s/spread.asp",
    "https://www.investopedia.com/terms/p/putcallparity.asp",
    "https://www.investopedia.com/terms/d/deltahedging.asp",
    "https://www.investopedia.com/terms/q/quantitativeanalysis.asp",
    "https://www.investopedia.com/terms/q/qualitativeanalysis.asp",
    "https://www.investopedia.com/articles/mutualfund/09/hedge-fundanalysis.asp",
    "https://www.investopedia.com/articles/trading/09/quant-strategies.asp",
    "https://www.investopedia.com/terms/f/fifo.asp",
]

# Asynchronous function to fetch documents
async def fetch_document(url):
    try:
        print(f"Fetching: {url}")
        """ 
        DESIGN CHOICE: 
        For simplicity, I will use the default WebBaseLoader.
        This removes the headache for parsing the url's html content.
        WebBaseLoader is a SYNCHRONOUS operation. 
        Consider the below option for more scalable document fetching.
        
        Alternative Option: 
        You may use aiohttp to make concurrent http requests for faster 
        processing but you'll also need to parse html.
        """
        loader = WebBaseLoader(url)
        docs = loader.load()
        return docs
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return []

    
# Asynchronous function to handle all URL fetching
async def fetch_all_documents(urls):
    tasks = [fetch_document(url) for url in urls]
    results = await asyncio.gather(*tasks)
    documents = [doc for doc_list in results for doc in doc_list]
    return documents


# Main processing function
async def main():
    # Fetch and process documents
    print("Starting document fetching...")
    documents = await fetch_all_documents(urls)

    # Validate documents
    if not documents:
        raise ValueError("No documents were successfully fetched. Check your URLs or internet connection.")

    # Split documents into smaller chunks
    print("Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = splitter.split_documents(documents)

    # Initialize OpenAI embeddings
    print("Initializing embeddings...")
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", openai_api_key=OPENAI_API_KEY)

    # Create or load Chroma vector store
    print("Creating Chroma vector store...")
    chroma_dir = "chroma_store"
    makedirs(chroma_dir, exist_ok=True)
    vectorstore = Chroma.from_documents(docs, embeddings, persist_directory=chroma_dir)

    # Save the vector store to disk
    print("Saving Chroma vector store...")
    vectorstore.persist()
    print("Indexing completed successfully!")

# Run the script
if __name__ == "__main__":
    asyncio.run(main())