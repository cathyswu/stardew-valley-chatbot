import asyncio
import json
import os
import re
from typing import Dict, List
from crawl4ai import AsyncWebCrawler, BestFirstCrawlingStrategy, CrawlerRunConfig, DomainFilter, FilterChain, LXMLWebScrapingStrategy, ContentTypeFilter
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.deep_crawling.filters import SEOFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

def create_filter_chain(allowed_domains: List[str], blocked_domains: List[str] = None, seo_keywords: List[str] = None) -> FilterChain:
    """Create filter chain with domain and content type filters"""
    if blocked_domains is None:
        blocked_domains = []
    
    filters = [
        DomainFilter(
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains
        ),
        ContentTypeFilter(allowed_types=["text/html"])
    ]

    if seo_keywords:
        filters.append(SEOFilter(threshold=0.5, keywords=seo_keywords))

    return FilterChain(filters)

def create_markdown_generator(prune_threshold: float = 0.4) -> DefaultMarkdownGenerator:
    """Create markdown generator with content pruning"""
    prune_filter = PruningContentFilter(
        threshold=prune_threshold,
        threshold_type="dynamic"
    )
    return DefaultMarkdownGenerator(content_filter=prune_filter)

def create_crawling_strategy(max_depth: int, max_pages: int, allowed_domains: List[str], 
                           blocked_domains: List[str] = None, include_external: bool = False) -> BestFirstCrawlingStrategy:
    """Create crawling strategy with specified parameters"""
    filter_chain = create_filter_chain(allowed_domains, blocked_domains)
    
    return BestFirstCrawlingStrategy(
        max_depth=max_depth,
        include_external=include_external,
        max_pages=max_pages,
        filter_chain=filter_chain
    )

def create_run_config(max_depth: int, max_pages: int, allowed_domains: List[str], 
                     blocked_domains: List[str] = None, css_selector: str = None,
                     excluded_tags: List[str] = None, prune_threshold: float = 0.4, seo_keywords: List[str] = None) -> CrawlerRunConfig:
    """Create crawler run configuration"""
    if excluded_tags is None:
        excluded_tags = ["form", "header", "footer", "nav", "aside", "script", "style"]
    
    md_generator = create_markdown_generator(prune_threshold)
    strategy = create_crawling_strategy(max_depth, max_pages, allowed_domains, blocked_domains, seo_keywords)
    
    config_params = {
        'markdown_generator': md_generator,
        'excluded_tags': excluded_tags,
        'exclude_external_links': True,
        'process_iframes': False,
        'remove_overlay_elements': True,
        'deep_crawl_strategy': strategy,
        'scraping_strategy': LXMLWebScrapingStrategy(),
        'verbose': True,
    }
    
    if css_selector:
        config_params['css_selector'] = css_selector
        
    return CrawlerRunConfig(**config_params)

def should_skip_content(markdown: str, url: str, skip_patterns: List[str]) -> bool:
    """Check if content should be skipped based on patterns"""
    if '.html/' in url:
        print(f"Skipped malformed URL: {url}")
        return True
    
    if len(markdown) < 10:
            print(f"❗Skipped empty/short content ({len(markdown)} chars): {url}")
            return True
    
    for pattern in skip_patterns:
        if pattern in markdown:
            print(f"Skipped content with pattern '{pattern}': {url}")
            return True
    
    return False

def process_results(results, skip_patterns: List[str]) -> Dict[str, str]:
    """Process crawl results and return content dictionary"""
    content_dict = {}
    
    for result in results:
        if result.success:
            url = result.url
            html = result.html

            if should_skip_content(html, url, skip_patterns):
                continue

            content_dict[url] = html
            print(f"Added: {url}")
        else:
            print(f"Crawl failed: {result.error_message}")
            print(f"Status code: {result.status_code}")
    
    return content_dict

def save_results_to_raw(content_dict: Dict[str, str], raw_dir: str = "data/raw"):
    """Save results as individual HTML files to data/raw directory"""
    os.makedirs(raw_dir, exist_ok=True)
    
    for url, content in content_dict.items():
        # Create filename from URL
        filename = url.replace("https://", "").replace("http://", "")
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)  # Replace invalid chars
        if not filename.endswith('.html'):
            filename += '.html'

        filepath = os.path.join(raw_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"Saved: {filepath}")
    
    print(f"All {len(content_dict)} files saved to {raw_dir}")

def save_results(content_dict: Dict[str, str], output_file: str):
    """Save results to JSON file"""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(content_dict, f, indent=2, ensure_ascii=False)
    print(f"Results saved to: {output_file}")

async def crawl_website(start_url: str, allowed_domains: List[str], blocked_domains: List[str] = None,
                       max_depth: int = 2, max_pages: int = 200, css_selector: str = None,
                       excluded_tags: List[str] = None, skip_patterns: List[str] = None,
                       prune_threshold: float = 0.4, seo_keywords: List[str] = None, raw_dir: str = "data/raw") -> Dict[str, str]:
    
    
    """Main crawling function"""
    if blocked_domains is None:
        blocked_domains = []
    if skip_patterns is None:
        skip_patterns = []
    if seo_keywords is None:
        seo_keywords = []
    
    print(f"Starting crawl for: {start_url}")
    
    browser_config = BrowserConfig(verbose=True)
    run_config = create_run_config(
        max_depth=max_depth,
        max_pages=max_pages,
        allowed_domains=allowed_domains,
        blocked_domains=blocked_domains,
        css_selector=css_selector,
        excluded_tags=excluded_tags,
        prune_threshold=prune_threshold,
        seo_keywords=seo_keywords
    )
    
    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun(url=start_url, config=run_config)
        
        content_dict = process_results(results, skip_patterns)
        
        print(f"\nTotal valid pages collected: {len(content_dict)}")
        
        if content_dict:
            save_results_to_raw(content_dict, raw_dir)
        
        return content_dict

async def main():
    stardew_config = {
        "start_url": "https://stardewvalleywiki.com/Stardew_Valley_Wiki",
        "allowed_domains": ["stardewvalleywiki.com"],
        "blocked_domains": 
            ["de.stardewvalleywiki.com", 
             "fr.stardewvalleywiki.com", 
             "es.stardewvalleywiki.com", 
             "ru.stardewvalleywiki.com",
             "pt.stardewvalleywiki.com",
             "it.stardewvalleywiki.com",
             "ja.stardewvalleywiki.com",
             "hu.stardewvalleywiki.com",
             "ko.stardewvalleywiki.com",
             "zh.stardewvalleywiki.com",
             "tr.stardewvalleywiki.com",
             "it.stardewvalleywiki.com",
             "hu.stardewvalleywiki.com"],
        "max_depth": 4,
        "max_pages": 500,
        "css_selector": "#mw-content-text",
        "prune_threshold": 0.35,
        "skip_patterns": [],
    }

    selected_config = stardew_config
    
    content_dict = await crawl_website(**selected_config)
    
    print(f"Crawling completed! Found {len(content_dict)} pages.")

if __name__ == "__main__":
    asyncio.run(main())
