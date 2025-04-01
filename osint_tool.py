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

import logging
import requests
import argparse
import json
import time
import re
import sys
import os
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
            rate_limit (int): Time to wait between requests in seconds
            timeout (int): Request timeout in seconds
            verbose (bool): Enable verbose output for debugging
        """
        self.target_name = target_name
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.verbose = verbose
        self.results = {}  # Dictionary to store all search results
        self.console = Console()  # Rich console for formatted output

        # User agent string to mimic a browser
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
        try:
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
        except Exception as e:
            logger.error(f"Error in search_data_breach_sites: {e}")
            return {}

    def search_people_directories(self):
        """
        Search for the target across people search and directory websites.

        These websites aggregate public records and may provide contact information,
        addresses, relatives, and other personal details.

        Returns:
            dict: Dictionary of people search directories with URLs and descriptions
        """
        try:
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
        except Exception as e:
            logger.error(f"Error in search_people_directories: {e}")
            return {}

    def search_professional_data(self):
        """
        Search for professional information about the target.

        This method generates links to platforms that may contain professional
        background, academic publications, business associations, and career info.

        Returns:
            dict: Dictionary of professional platforms with URLs and descriptions
        """
        try:
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
        except Exception as e:
            logger.error(f"Error in search_professional_data: {e}")
            return {}

    def search_public_records(self):
        """
        Search for public records related to the target.

        This method provides links to resources that maintain databases of official
        public records such as voter registrations, property records, and corporate filings.

        Returns:
            dict: Dictionary of public record sources with URLs and descriptions
        """
        try:
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
        except Exception as e:
            logger.error(f"Error in search_public_records: {e}")
            return {}

    def search_web_presence(self):
        """
        Search for general web presence of the target.

        This method generates links to search engines and web archives that can
        provide a broad overview of the target's online presence and history.

        Returns:
            dict: Dictionary of search engines and web archives with URLs and descriptions
        """
        try:
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
        except Exception as e:
            logger.error(f"Error in search_web_presence: {e}")
            return {}

    def search_images(self):
        """
        Search for images of the target.

        This method provides links to image search engines and facial recognition
        services that might find photos of the target online.

        Returns:
            dict: Dictionary of image search engines with URLs and descriptions
        """
        try:
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
        except Exception as e:
            logger.error(f"Error in search_images: {e}")
            return {}

    def search_dark_web(self):
        """
        Generate search URLs for the target across dark web search engines.

        This method creates links to search results on various dark web search engines
        where the target might have profiles or mentions.

        Returns:
            dict: Dictionary of dark web platforms with their search URLs and descriptions
        """
        try:
            # Define dark web search engines and their search URL patterns
            dark_web_search_engines = {
                "Ahmia": f"https://ahmia.fi/search/?q={quote_plus(self.target_name)}",
                "DarkSearch": f"https://darksearch.io/search?query={quote_plus(self.target_name)}",
            }

            # Build results dictionary
            results = {}
            for platform, url in dark_web_search_engines.items():
                results[platform] = {
                    "url": url,
                    "description": f"Search for {self.target_name} on {platform}"
                }

            return results
        except Exception as e:
            logger.error(f"Error in search_dark_web: {e}")
            return {}

    def search_reverse_phone(self):
        """
        Generate search URLs for reverse phone lookup.

        This method creates links to search results on various reverse phone lookup platforms.

        Returns:
            dict: Dictionary of reverse phone lookup platforms with their search URLs and descriptions
        """
        try:
            # Define reverse phone lookup platforms and their search URL patterns
            phone_lookup_sites = {
                "TrueCaller": f"https://www.truecaller.com/search/us/{quote_plus(self.target_name)}",
                "AnyWho": f"https://www.anywho.com/phone/{quote_plus(self.target_name)}",
            }

            # Build results dictionary
            results = {}
            for platform, url in phone_lookup_sites.items():
                results[platform] = {
                    "url": url,
                    "description": f"Reverse phone lookup for {self.target_name} on {platform}"
                }

            return results
        except Exception as e:
            logger.error(f"Error in search_reverse_phone: {e}")
            return {}

    def search_email_addresses(self):
        """
        Generate search URLs for email address lookup.

        This method creates links to search results on various email lookup platforms.

        Returns:
            dict: Dictionary of email lookup platforms with their search URLs and descriptions
        """
        try:
            # Define email lookup platforms and their search URL patterns
            email_lookup_sites = {
                "Hunter.io": f"https://hunter.io/search/{quote_plus(self.target_name)}",
                "EmailRep": f"https://emailrep.io/{quote_plus(self.target_name)}",
            }

            # Build results dictionary
            results = {}
            for platform, url in email_lookup_sites.items():
                results[platform] = {
                    "url": url,
                    "description": f"Email lookup for {self.target_name} on {platform}"
                }

            return results
        except Exception as e:
            logger.error(f"Error in search_email_addresses: {e}")
            return {}

    def search_geolocation(self):
        """
        Generate search URLs for IP address geolocation.

        This method creates links to search results on various geolocation platforms.

        Returns:
            dict: Dictionary of geolocation platforms with their search URLs and descriptions
        """
        try:
            # Define geolocation platforms and their search URL patterns
            geolocation_sites = {
                "IP2Location": f"https://www.ip2location.com/demo/{quote_plus(self.target_name)}",
                "MaxMind": f"https://www.maxmind.com/en/geoip-demo/{quote_plus(self.target_name)}",
            }

            # Build results dictionary
            results = {}
            for platform, url in geolocation_sites.items():
                results[platform] = {
                    "url": url,
                    "description": f"Geolocation lookup for {self.target_name} on {platform}"
                }

            return results
        except Exception as e:
            logger.error(f"Error in search_geolocation: {e}")
            return {}

    def search_blockchain(self):
        """
        Generate search URLs for blockchain and cryptocurrency transactions.

        This method creates links to search results on various blockchain exploration platforms.

        Returns:
            dict: Dictionary of blockchain platforms with their search URLs and descriptions
        """
        try:
            # Define blockchain platforms and their search URL patterns
            blockchain_sites = {
                "Blockchain.info": f"https://www.blockchain.com/btc/address/{quote_plus(self.target_name)}",
                "Etherscan": f"https://etherscan.io/address/{quote_plus(self.target_name)}",
            }

            # Build results dictionary
            results = {}
            for platform, url in blockchain_sites.items():
                results[platform] = {
                    "url": url,
                    "description": f"Blockchain transactions for {self.target_name} on {platform}"
                }

            return results
        except Exception as e:
            logger.error(f"Error in search_blockchain: {e}")
            return {}

    def run_all_searches(self):
        """
        Run all search methods and compile results.

        This method executes all the individual search methods and combines
        their results into a single structured dictionary.

        Returns:
            dict: Combined dictionary of all search results categorized by type
        """
        try:
            # Use Rich progress spinner to show activity while searches are running
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("[cyan]Running OSINT searches...", total=12)

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

                self.results["Dark Web"] = self.search_dark_web()
                progress.update(task, advance=1)

                self.results["Reverse Phone Lookup"] = self.search_reverse_phone()
                progress.update(task, advance=1)

                self.results["Email Addresses"] = self.search_email_addresses()
                progress.update(task, advance=1)

                self.results["Geolocation"] = self.search_geolocation()
                progress.update(task, advance=1)

                self.results["Blockchain"] = self.search_blockchain()
                progress.update(task, advance=1)

            return self.results
        except Exception as e:
            logger.error(f"Error in run_all_searches: {e}")
            return {}

    def display_results(self):
        """
        Display the collected OSINT information in a formatted table.

        This method uses the Rich library to create nicely"
        """
