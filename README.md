
<parameter name="content"># OSINT Information Gathering Tool

A Python-based command-line tool for gathering Open Source Intelligence (OSINT) information about a target individual by generating links to various online resources.

## Overview

This tool helps streamline the initial phase of OSINT research by automatically generating links to search results across multiple categories of online resources. It provides a structured approach to open source intelligence gathering for legitimate research purposes.

## Features

- Searches across 7 major categories of OSINT resources:
  - Social Media (Twitter/X, LinkedIn, Facebook, Instagram, Reddit, GitHub)
  - Data Breach Sites (Have I Been Pwned, BreachDirectory, DeHashed)
  - People Directories (Whitepages, Spokeo, PeopleFinders, etc.)
  - Professional Data (Google Scholar, ResearchGate, Crunchbase)
  - Public Records (voter records, corporate filings, SEC documents)
  - General Web Presence (search engines, Wayback Machine)
  - Images (Google Images, Bing Images, Yandex, facial recognition services)
- Displays results in formatted console tables
- Exports results to JSON for further analysis
- Command-line interface with customizable parameters

## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)

### Setup

1. Clone this repository or download the script:

```bash
git clone https://github.com/yourusername/osint-tool.git
cd osint-tool
```

2. Install the required dependencies:

```bash
pip install requests beautifulsoup4 rich
```

## Usage

### Basic Usage

```bash
python osint_tool.py "John Smith"
```

### Command Line Options

```
python osint_tool.py [-h] [-r RATE_LIMIT] [-t TIMEOUT] [-o OUTPUT] [-v] name
```

#### Arguments:

- `name`: The name of the target to gather information about (required)
- `-r, --rate-limit`: Time to wait between requests in seconds (default: 1)
- `-t, --timeout`: Request timeout in seconds (default: 10)
- `-o, --output`: Custom output file for results (default: automatically generated)
- `-v, --verbose`: Enable verbose output for debugging
- `-h, --help`: Show help message

### Examples

Search for information about "Jane Doe":
```bash
python osint_tool.py "Jane Doe"
```

Export results to a specific file:
```bash
python osint_tool.py "Jane Doe" --output jane_results.json
```

Use custom rate limiting:
```bash
python osint_tool.py "Jane Doe" --rate-limit 2
```

## Output

The tool generates two types of output:

1. **Console Output**: Formatted tables showing all search categories and sources
2. **JSON File**: A structured JSON file containing all search results

Example JSON structure:
```json
{
  "Social Media": {
    "Twitter/X": {
      "url": "https://twitter.com/search?q=Jane%20Doe&src=typed_query&f=user",
      "description": "Potential Twitter/X profiles for Jane Doe"
    },
    ...
  },
  ...
}
```

## Legal and Ethical Considerations

This tool is designed for legitimate research purposes only. It does not perform any actual scraping or data collection, but rather generates links to publicly accessible search pages.

When conducting OSINT research:

- Respect privacy and legal boundaries
- Follow the terms of service for each platform
- Use the information obtained ethically and responsibly
- Be aware of applicable laws regarding information gathering in your jurisdiction

## Limitations

- The tool only generates search links and does not perform actual data collection
- Results require manual verification and investigation
- Some linked services may require registration or authentication
- Search effectiveness depends on the uniqueness of the target's name

## Future Enhancements

Potential future improvements:

- Email and username search capabilities
- Location-based search options
- Historical data search integration
- Automated result verification
- Result correlation and analysis features

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is provided for educational and research purposes only. The author assumes no liability for any misuse of this software or for any damages that might result from its use.
</parameter>
</invoke>
