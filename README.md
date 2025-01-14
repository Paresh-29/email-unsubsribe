# Gmail Unsubscribe Automation Tool

This tool automates the process of managing unwanted emails by identifying and interacting with unsubscribe links in your Gmail inbox. It leverages the IMAP protocol to access emails, extracts unsubscribe links from HTML content, and optionally interacts with these links to streamline the process.

## Features
- **Email Search**: Searches for emails containing the keyword "unsubscribe."
- **Link Extraction**: Parses email content to extract unsubscribe links.
- **Automated Unsubscribe**: Attempts to visit the unsubscribe links to remove subscriptions.
- **Logging**: Saves all unsubscribe links to a file (`links.txt`) for future reference.

## Requirements
- **Python Libraries**:
  - `dotenv`
  - `imaplib` (built-in)
  - `email` (built-in)
  - `BeautifulSoup` (from `bs4`)
  - `requests`
- A `.env` file with the following variables:
  ```
  EMAIL=<your-email-address>
  PASSWORD=<your-email-password>
  ```

## How It Works
1. Connects to your Gmail account using IMAP.
2. Searches for emails containing the word "unsubscribe" in the body.
3. Extracts unsubscribe links from the HTML content of the emails.
4. Attempts to visit each link (to unsubscribe automatically).
5. Saves the list of all found unsubscribe links to a file (`links.txt`).

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/Paresh-29/email-unsubscribe.git
   ```
2. Navigate to the project directory:
   ```bash
   cd email-unsubscribe
   ```
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add your email credentials:
   ```plaintext
   EMAIL=<your-email-address>
   PASSWORD=<your-email-password>
   ```

## Usage
Run the script with:
```bash
python main.py
```

## Notes
- Ensure that IMAP access is enabled for your Gmail account.
- Use an app password if you're using Gmail with 2-factor authentication.
- Review the `links.txt` file to manually verify any links if needed.
