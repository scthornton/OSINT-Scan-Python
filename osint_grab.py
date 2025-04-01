import logging
import requests
import argparse
import json
import time
import re
import sys
import os
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OSINTTool:
    """
    A tool for gathering Open Source Intelligence (OSINT) information about a target.
    
    This class provides methods to search for a target across various online platforms
    and resources, generating links that can be manually investigated. It doesn't
    actually scrape or extract data from these sites due to legal and ethical considerations,
    but instead provides organized starting points for manual OSINT research.
    """
    
    def __init__(self, target_name, rate_limit=1, timeout=10, verbose=False):
        """
        Initialize the OSINT Tool with target information and settings.
        
        Args:
            target_name (str): The name of the target to search for
            rate_limit (int): Time to wait between requests in seconds (for future implementations)
            timeout (int): Request timeout in seconds (for future implementations)
            verbose (bool): Enable verbose output for debugging
        """
        self.target_name = target_name
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.verbose = verbose
        self.results = {}  # Dictionary to store all search results
        self.console = Console()  # Rich console for formatted output
        
        # User agent string to mimic a browser (for future implementations)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        }
    
    def search_social_media(self):
        """
        Generate search URLs for the target across major social media platforms.
        
        This method creates links to search results on various social media platforms
        where the target might have profiles or be mentioned.
        
        Returns:
            dict: Dictionary of social media platforms with their search URLs and descriptions
        """
        try:
            # Define social media platforms and their search URL patterns
            social_platforms = {
                "Twitter/X": f"https://twitter.com/search?q={quote_plus(self.target_name)}&src=typed_query&f=user",
                "LinkedIn": f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(self.target_name)}",
                "Facebook": f"https://www.facebook.com/search/people/?q={quote_plus(self.target_name)}",
                "Instagram": f"https://www.instagram.com/explore/tags/{quote_plus(self.target_name.replace(' ', ''))}",
                "Reddit": f"https://www.reddit.com/search/?q={quote_plus(self.target_name)}&type=user",
                "GitHub": f"https://github.com/search?q={quote_plus(self.target_name)}&type=users",
            }
            
            # Build results dictionary
            results = {}
            for platform, url in social_platforms.items():
                results[platform] = {
                    "url": url,
                    "description": f"Potential {platform} profiles for {self.target_name}"
                }
            
            return results
        except Exception as e:
            logger.error(f"Error in search_social_media: {e}")
            return {}

    # Similar modifications can be made to other methods...

def main():
    """
    Main function to handle command line interface.
    
    This function parses command line arguments, initializes the OSINT tool,
    and manages the execution flow including error handling.
    """
    # Set up command line argument parser
    parser = argparse.ArgumentParser(
        description="OSINT Information Gathering Tool",
        epilog="Example: python osint_tool.py 'John Smith' --output results.json"
    )
    
    # Add command line arguments
    parser.add_argument("name", 
                       help="Name of the target to gather information about")
    parser.add_argument("-r", "--rate-limit", 
                       type=int, default=1, 
                       help="Time to wait between requests in seconds (default: 1)")
    parser.add_argument("-t", "--timeout", 
                       type=int, default=10,
                       help="Request timeout in seconds (default: 10)")
    parser.add_argument("-o", "--output", 
                       type=str, 
                       help="Output file for the results (default: automatically generated)")
    parser.add_argument("-v", "--verbose", 
                       action="store_true",
                       help="Enable verbose output")
    
    # Parse the arguments
    args = parser.parse_args()
    
    try:
        # Initialize and run the OSINT tool
        osint = OSINTTool(
            args.name,
            rate_limit=args.rate_limit,
            timeout=args.timeout,
            verbose=args.verbose
        )
        
        # Create console for output
        console = Console()
        console.print(f"\n[bold cyan]Starting OSINT search for:[/bold cyan] {args.name}\n")
        
        # Run all searches
        osint.run_all_searches()
        
        # Display results in formatted tables
        osint.display_results()
        
        # Export results to JSON file
        if args.output:
            osint.export_results(args.output)
        else:
            osint.export_results()
            
    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C)
        console = Console()
        console.print("\n[bold red]Search interrupted by user[/bold red]")
        sys.exit(1)
    except Exception as e:
        # Handle other exceptions
        console = Console()
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        if args.verbose:
            # Print full traceback if verbose mode is enabled
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)

# Entry point for script execution
if __name__ == "__main__":
    main()
