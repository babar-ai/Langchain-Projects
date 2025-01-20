
# #old method 
# from langchain.document_loaders import PyPDFLoader
# Loader = PyPDFLoader('F:\summer work\maktek\Ai Interns Agreement.docx (2).pdf')
# pages = Loader.load()
# print('total number of pages :',len(pages))
# page = pages[0]
# print(page.page_content[0:500]) #page_content is an attribute of the page object that contains the text extracted from that page.

#latest method to read pdf

from langchain_community.document_loaders import PyPDFLoader
Loader = PyPDFLoader('F:\summer work\maktek\Ai Interns Agreement.docx (2).pdf')
pages = Loader.load()
print('total number of pages :',len(pages))

#differences

# Summary
# langchain_community.document_loaders: Likely a community or extended version with potentially more experimental or specialized features.
# langchain.document_loaders: The main, official version provided by LangChain's core library, generally more stable and widely supported.