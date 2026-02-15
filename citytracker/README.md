# HOPPy-4-Dashboards

Python dashboards for NYC Open Data analysis.

## Setup

### Prerequisites
- Python 3.14 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up your environment variables:
   ```bash
   cp .env.example .env
   ```

3. Get your Socrata API token:
   - Visit https://data.cityofnewyork.us/profile/edit/developer_settings
   - Sign in and create a new app token
   - Copy the token

4. Edit `.env` and add your token:
   ```bash
   SOCRATA_APP_TOKEN=your_actual_token_here
   ```

### Usage

```python
import os
from dotenv import load_dotenv
from sodapy import Socrata

load_dotenv()
token = os.getenv("SOCRATA_APP_TOKEN")

client = Socrata("data.cityofnewyork.us", token)
# Fetch data...
```

## Why Use an App Token?

Socrata API rate limits:
- **Without token**: 1,000 requests/day
- **With app token**: 10,000 requests/day

App tokens are free and easy to obtain.

## Finding Dataset IDs

NYC Open Data dataset IDs are the 4x4 code in the dataset URL:
- URL: `https://data.cityofnewyork.us/dataset/abc-1234`
- Dataset ID: `abc-1234`

Popular datasets:
- 311 Service Requests: `erm2-nwe9`

## Troubleshooting

**Error: "No token found"**
- Make sure you created a `.env` file (copy from `.env.example`)
- Verify your token is set correctly in `.env`
- Don't use quotes around the token value

**Error: "python-dotenv module not found"**
- Run `uv sync` to install all dependencies