# from dotenv import load_dotenv
# import imaplib
# import email
# import os
# from bs4 import BeautifulSoup
# import chardet

# load_dotenv()

# username = os.getenv("EMAIL")
# password = os.getenv("PASSWORD")

# # connect to mail
# def connect_to_mail():
#     mail = imaplib.IMAP4_SSL("imap.gmail.com")
#     mail.login(username, password)
#     mail.select("inbox")
#     return mail


# def extract_links_from_html(html_content):
#     soup = BeautifulSoup(html_content, "html.parser")
#     links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]
#     return links

# def click_link(Link):
#     try:
#         response = requests.get(Link)
#         if response.status_code == 200:
#             print(f"Successfully clicked link: {Link}")
#         else:
#             print("failed to visit link", Link, "error code", response.status_code)
#     except Exception as e:
#         print("Error with", Link, str(e))



# def decode_email_content(raw_content):
#     try:
#         detected = chardet.detect(raw_content)
#         return raw_content.decode(detected['encoding'] or 'utf-8', errors="replace")
#     except Exception:
#         encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
#         for encoding in encodings:
#             try:
#                 return raw_content.decode(encoding, errors="replace")
#             except:
#                 continue
#         return raw_content.decode('utf-8', errors="replace")

# # search for emails with unsubscribe in the subject
# def search_for_emails():
#     mail = connect_to_mail()
#     _, search_data = mail.search(None, '(BODY "unsubscribe")')
#     data = search_data[0].split()
    
#     links = []
    
#     for num in data:
#         _, data = mail.fetch(num, "(RFC822)")
#         msg = email.message_from_bytes(data[0][1])
        
#         if msg.is_multipart():
#             for part in msg.walk():
#                 if part.get_content_type() == "text/html":
#                     raw_content = part.get_payload(decode=True)
#                     html_content = decode_email_content(raw_content)
#                     links.extend(extract_links_from_html(html_content))
#         else:
#             content_type = msg.get_content_type()
#             raw_content = msg.get_payload(decode=True)
            
#             if content_type == "text/html":
#                 content = decode_email_content(raw_content)
#                 links.extend(extract_links_from_html(content))
#     mail.logout()
#     return links

# def save_links(Links):
#     with open("links.txt", "w") as f:
#         f.write("\n".join(Links))


# links = search_for_emails()
# for link in links:
#     click_link(link)

# save_links(links)


from dotenv import load_dotenv
import imaplib
import email
import os
from bs4 import BeautifulSoup
import requests
load_dotenv()
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# connect to mail
def connect_to_mail():
    print("Connecting to Gmail...")
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    print("Successfully connected to mail")
    return mail

def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]
    print(f"Found {len(links)} unsubscribe links in HTML")
    return links

def click_link(Link):
    try:
        print(f"Attempting to click link: {Link}")
        response = requests.get(Link)
        if response.status_code == 200:
            print(f"Successfully clicked link: {Link}")
        else:
            print("Failed to visit link", Link, "error code", response.status_code)
    except Exception as e:
        print("Error with", Link, str(e))

# search for emails with unsubscribe in the subject
def search_for_emails():
    mail = connect_to_mail()
    print("Searching for emails with 'unsubscribe'...")
    _, search_data = mail.search(None, '(BODY "unsubscribe")')
    data = search_data[0].split()
    print(f"Found {len(data)} emails to process")
    links = []
    for num in data:
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    try:
                        html_content = part.get_payload(decode=True).decode()
                        links.extend(extract_links_from_html(html_content))
                    except Exception as e:
                        print(f"Error decoding HTML part: {e}")
        else:
            content_type = msg.get_content_type()
            try:
                content = msg.get_payload(decode=True).decode()
                if content_type == "text/html":
                    links.extend(extract_links_from_html(content))
            except Exception as e:
                print(f"Error decoding email content: {e}")
    
    mail.logout()
    print(f"Total unique unsubscribe links found: {len(links)}")
    return links

def save_links(Links):
    with open("links.txt", "w") as f:
        f.write("\n".join(Links))
    print(f"Saved {len(Links)} links to links.txt")

links = search_for_emails()
for link in links:
    click_link(link)
save_links(links)