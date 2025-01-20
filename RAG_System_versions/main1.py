import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from some_module import CharacterTextSplitter, HuggingFaceEmbeddings, FAISS, Tool, ChatGroq, initialize_agent, load_tools  # Adjust the import based on actual module names

# Helper function to normalize URLs
def normalize_url(url):
    parsed_url = urlparse(url)
    # Reconstruct the URL without query parameters, fragment, etc.
    normalized_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return normalized_url.rstrip('/')

def Is_internal_link(url, start_url):
    # urllib.parse module to break down a URL into its components. One of these components is netloc, which represents the domain (e.g., example.com).
    base_netloc = urlparse(start_url).netloc
    target_netloc = urlparse(url).netloc
    # If the netloc (domain) of both is the same, it's an internal link
    return base_netloc == target_netloc

# Scrape page function
def Scrape_page(url, start_url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        '''The 'html.parser' is a straightforward, built-in option that BeautifulSoup uses to parse HTML content, converting it into a BeautifulSoup object. This object allows you to navigate and manipulate the HTML document as a tree structure, making it easy to extract information, modify tags, and more.'''
        
        # Extract text from the page
        page_text = soup.get_text(separator='\n')
        '''The get_text() method in BeautifulSoup extracts all the text from the HTML document, ignoring the HTML tags'''
        
        # Find all the internal links
        internal_links = set()
        Links = soup.find_all('a', href=True)
        
        for link in Links:
            href = link['href']
            # Convert relative URLs to absolute
            full_urls = urljoin(start_url, href)
            '''A relative URL provides a path to a resource relative to the current page’s URL. It omits the domain and protocol, focusing only on the path within the same site.'''
            full_url = normalize_url(full_urls)
            
            if Is_internal_link(full_url, start_url):
                internal_links.add(full_url)
        
        return page_text, internal_links
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return "", set()

# Scrape site function
def scrape_site(start_url):
    scraped_content = {}
    urls_to_scrape = set([start_url])  # Use a set for uniqueness
    scraped_urls = set()
    
    while urls_to_scrape:
        url = urls_to_scrape.pop()
        if url not in scraped_urls:
            print(f"Scraping {url}")
        
        page_text, internal_links = Scrape_page(url, start_url)
        
        scraped_content[url] = page_text
        urls_to_scrape.update(internal_links - scraped_urls)
        scraped_urls.add(url)
        time.sleep(1)  # Be polite and avoid too many requests in a short time

    return scraped_content

# Function to process URLs
def Process_data(scraped_data):
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=1500, chunk_overlap=200)
    docs = text_splitter.split_text(scraped_data)
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_texts(docs, embedding_model)
    return db

# Define the start URL
start_url = "https://www.uetmardan.edu.pk"
# Scrape the site
scraped_data = scrape_site(start_url)
# Process the scraped data
vector_db = Process_data(scraped_data)

# Create retriever tool
retriever = vector_db.as_retriever()
retriever_tool = Tool(
    name="vectordb",
    func=retriever.invoke,
    description="Use this tool for retrieving information about UET Mardan."
)

# Pre-prompt to define the salesperson persona
pre_prompt = '''
You are a highly knowledgeable and friendly salesperson at the University of Engineering and Technology Mardan (UET Mardan). Your goal is to help potential students and their parents make informed decisions about enrolling in the university. You understand the needs and concerns of prospective students, and you provide clear, accurate, and persuasive information to guide them toward making a decision that suits their educational goals. Be sure to highlight the unique advantages of UET Mardan and how it meets their needs.
'''

# Initialize the LLM
llm = ChatGroq(
    model_name="llama-3.1-70b-versatile",
    groq_api_key= GROQ_API_KEY,
    temperature=0,
    verbose=True
)

# Load additional tools
tools = load_tools(["ddg-search", "llm-math", "wikipedia"], llm=llm)
tools.append(retriever_tool)

# Initialize zero-shot agent with the pre-prompt
zero_shot_agent = initialize_agent(
    agent="zero-shot-react-description",
    tools=tools,
    prompt=pre_prompt,
    llm=llm,
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

# Example query to the agent
response = zero_shot_agent.run("Can you tell me why UET Mardan is the best choice for engineering students?")
print(response)
