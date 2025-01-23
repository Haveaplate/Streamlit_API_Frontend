from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

def scrape_website(website):
    chrome_driver_path = ""
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service = Service(chrome_driver_path), options = options)

    try:
        driver.get(website)

        html = driver.page_source
        time.sleep(5)

        return html
    
    finally:
        driver.quit()

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body

    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator = "\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content(dom_content, max_length = 6000):
    return [dom_content[i : i + max_length] for i in range (0, len(dom_content), max_length)]

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

model = OllamaLLM(model = "llama3")

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start = 1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )

        print(f"Parsed batch {i} of {len(dom_chunks)}")
        parsed_results.append(response)

    return "\n".join(parsed_results)

