#!/usr/bin/env python3
"""
OSINT Information Gathering Tool
--------------------------------
This script allows you to search for information about a person across multiple
open-source intelligence resources. It generates and organizes links to various 
online platforms where information about the target might be available.

Usage:
    python osint_tool.py "John Smith"
    python osint_tool.py "Jane Doe" --output results.json
    python osint_tool.py "Alex Johnson" --rate-limit 2 --timeout 15 --verbose

Dependencies:
    - requests: For HTTP requests (though not used for actual requests in this implementation)
    - beautifulsoup4: For parsing HTML (for future implementations)
    - rich: For formatted console output
"""

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
    
    def search_data_breach_sites(self):
        """
        Generate links to check if the target's information appears in data breaches.
        
        This method provides URLs to services that maintain databases of leaked
        credentials and personal information from data breaches.
        
        Note: 
            Some of these services require registration/authentication to access
            their full functionality.
        
        Returns:
            dict: Dictionary of breach checking sites with URLs and descriptions
        """
        # Define data breach sites and their search URLs
        breach_sites = {
            "Have I Been Pwned": f"https://haveibeenpwned.com/",
            "BreachDirectory": f"https://breachdirectory.org/",
            "DeHashed": f"https://dehashed.com/search?query={quote_plus(self.target_name)}",
        }
        
        # Build results dictionary
        results = {}
        for site, url in breach_sites.items():
            results[site] = {
                "url": url,
                "description": f"Check if {self.target_name} appears in known data breaches"
            }
            
        return results
    
    def search_people_directories(self):
        """
        Search for the target across people search and directory websites.
        
        These websites aggregate public records and may provide contact information,
        addresses, relatives, and other personal details.
        
        Returns:
            dict: Dictionary of people search directories with URLs and descriptions
        """
        # Define people search directories and their URL patterns
        directories = {
            "Whitepages": f"https://www.whitepages.com/name/{quote_plus(self.target_name.replace(' ', '-'))}",
            "Spokeo": f"https://www.spokeo.com/{quote_plus(self.target_name.replace(' ', '-'))}",
            "PeopleFinders": f"https://www.peoplefinders.com/people/{quote_plus(self.target_name.replace(' ', '-'))}",
            "TruePeopleSearch": f"https://www.truepeoplesearch.com/results?name={quote_plus(self.target_name)}",
            "FastPeopleSearch": f"https://www.fastpeoplesearch.com/name/{quote_plus(self.target_name.replace(' ', '-'))}",
            "411.com": f"https://www.411.com/name/{quote_plus(self.target_name.replace(' ', '-'))}",
        }
        
        # Build results dictionary
        results = {}
        for directory, url in directories.items():
            results[directory] = {
                "url": url,
                "description": f"Public records and contact information for {self.target_name}"
            }
            
        return results
    
    def search_professional_data(self):
        """
        Search for professional information about the target.
        
        This method generates links to platforms that may contain professional
        background, academic publications, business associations, and career info.
        
        Returns:
            dict: Dictionary of professional platforms with URLs and descriptions
        """
        # Define professional data sources and their URL patterns
        professional_sites = {
            "Google Scholar": f"https://scholar.google.com/scholar?q={quote_plus(self.target_name)}",
            "ResearchGate": f"https://www.researchgate.net/search/researcher?q={quote_plus(self.target_name)}",
            "ORCID": f"https://orcid.org/orcid-search/search?searchQuery={quote_plus(self.target_name)}",
            "Crunchbase": f"https://www.crunchbase.com/textsearch?q={quote_plus(self.target_name)}&entity=people",
            "Bloomberg": f"https://www.bloomberg.com/search?query={quote_plus(self.target_name)}",
        }
        
        # Build results dictionary
        results = {}
        for site, url in professional_sites.items():
            results[site] = {
                "url": url,
                "description": f"Professional information, publications, and business data for {self.target_name}"
            }
            
        return results
    
    def search_public_records(self):
        """
        Search for public records related to the target.
        
        This method provides links to resources that maintain databases of official
        public records such as voter registrations, property records, and corporate filings.
        
        Returns:
            dict: Dictionary of public record sources with URLs and descriptions
        """
        # Define public record sources and their URL patterns
        public_records = {
            "SearchQuarry": f"https://www.searchquarry.com/namesearch/",
            "VoterRecords": f"https://voterrecords.com/voters/{quote_plus(self.target_name.replace(' ', '-'))}",
            "OpenCorporates": f"https://opencorporates.com/officers?utf8=%E2%9C%93&q={quote_plus(self.target_name)}&commit=Search",
            "SEC Edgar": f"https://www.sec.gov/cgi-bin/browse-edgar?company={quote_plus(self.target_name)}&owner=exclude&action=getcompany",
            "Property Records": f"https://www.propertyshark.com/mason/Search/",
        }
        
        # Build results dictionary
        results = {}
        for record_type, url in public_records.items():
            results[record_type] = {
                "url": url,
                "description": f"Public records and official filings that may mention {self.target_name}"
            }
            
        return results
    
    def search_web_presence(self):
        """
        Search for general web presence of the target.
        
        This method generates links to search engines and web archives that can
        provide a broad overview of the target's online presence and history.
        
        Returns:
            dict: Dictionary of search engines and web archives with URLs and descriptions
        """
        # Define search engines and their URL patterns
        web_searches = {
            "Google": f"https://www.google.com/search?q={quote_plus(self.target_name)}",
            "Bing": f"https://www.bing.com/search?q={quote_plus(self.target_name)}",
            "DuckDuckGo": f"https://duckduckgo.com/?q={quote_plus(self.target_name)}",
            "Baidu": f"https://www.baidu.com/s?wd={quote_plus(self.target_name)}",
            "Yandex": f"https://yandex.com/search/?text={quote_plus(self.target_name)}",
            "Wayback Machine": f"https://web.archive.org/web/*/{quote_plus(self.target_name)}",
        }
        
        # Build results dictionary
        results = {}
        for engine, url in web_searches.items():
            results[engine] = {
                "url": url,
                "description": f"General web search for {self.target_name}"
            }
            
        return results
    
    def search_images(self):
        """
        Search for images of the target.
        
        This method provides links to image search engines and facial recognition
        services that might find photos of the target online.
        
        Returns:
            dict: Dictionary of image search engines with URLs and descriptions
        """
        # Define image search engines and their URL patterns
        image_searches = {
            "Google Images": f"https://www.google.com/search?q={quote_plus(self.target_name)}&tbm=isch",
            "Bing Images": f"https://www.bing.com/images/search?q={quote_plus(self.target_name)}",
            "Yandex Images": f"https://yandex.com/images/search?text={quote_plus(self.target_name)}",
            "TinEye": f"https://tineye.com/",  # Requires manual image upload
            "PimEyes": f"https://pimeyes.com/en",  # Requires manual image upload
        }
        
        # Build results dictionary
        results = {}
        for engine, url in image_searches.items():
            results[engine] = {
                "url": url,
                "description": f"Image search for {self.target_name}" 
            }
            
        return results
    
    def run_all_searches(self):
        """
        Run all search methods and compile results.
        
        This method executes all the individual search methods and combines
        their results into a single structured dictionary.
        
        Returns:
            dict: Combined dictionary of all search results categorized by type
        """
        # Use Rich progress spinner to show activity while searches are running
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("[cyan]Running OSINT searches...", total=7)
            
            # Collect results from all search methods
            self.results["Social Media"] = self.search_social_media()
            progress.update(task, advance=1)
            
            self.results["Data Breach Sites"] = self.search_data_breach_sites()
            progress.update(task, advance=1)
            
            self.results["People Directories"] = self.search_people_directories()
            progress.update(task, advance=1)
            
            self.results["Professional Data"] = self.search_professional_data()
            progress.update(task, advance=1)
            
            self.results["Public Records"] = self.search_public_records()
            progress.update(task, advance=1)
            
            self.results["Web Presence"] = self.search_web_presence()
            progress.update(task, advance=1)
            
            self.results["Images"] = self.search_images()
            progress.update(task, advance=1)
        
        return self.results
    
    def display_results(self):
        """
        Display the collected OSINT information in a formatted table.
        
        This method uses the Rich library to create nicely formatted tables
        showing all the search results grouped by category.
        """
        # Print header with target name
        self.console.print(f"\n[bold green]OSINT Results for:[/bold green] [bold yellow]{self.target_name}[/bold yellow]\n")
        
        # Loop through each category and create a table for its results
        for category, sources in self.results.items():
            self.console.print(f"[bold blue]{category}[/bold blue]")
            
            # Create and format the table
            table = Table(show_header=True, header_style="bold")
            table.add_column("Source")
            table.add_column("URL")
            table.add_column("Description")
            
            # Add rows for each source in the category
            for source, data in sources.items():
                table.add_row(
                    source,
                    data["url"],
                    data["description"]
                )
            
            # Display the table and add spacing
            self.console.print(table)
            self.console.print("")
    
    def export_results(self, filename=None):
        """
        Export the results to a JSON file.
        
        This method saves all the collected search results to a JSON file for
        further analysis or reference.
        
        Args:
            filename (str, optional): Filename to save the results to.
                If not provided, a filename is generated based on the target name.
        """
        if filename is None:
            # Generate a filename based on the target name and timestamp
            # Replace non-alphanumeric characters with underscore
            safe_name = re.sub(r'[^\w]', '_', self.target_name.lower())
            timestamp = int(time.time())
            filename = f"osint_{safe_name}_{timestamp}.json"
        
        # Write results to the JSON file
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        # Confirm to the user
        self.console.print(f"[bold green]Results exported to:[/bold green] {filename}")


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
