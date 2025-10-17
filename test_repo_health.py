#!/usr/bin/env python3
"""
Repository Health Check - Browser Automation Test
Tests the renamed 'agents' repository for correct branding, links, and functionality
"""

import asyncio
import sys
from playwright.async_api import async_playwright

class RepoHealthChecker:
    def __init__(self):
        self.repo_url = "https://github.com/minuetai/agents"
        self.pages_url = "https://minuetai.github.io/agents/"
        self.results = []
        self.failed = False

    def log_result(self, test_name, status, details=""):
        """Log test result"""
        symbol = "✅" if status else "❌"
        self.results.append(f"{symbol} {test_name}: {details}")
        if not status:
            self.failed = True
        print(f"{symbol} {test_name}: {details}")

    async def test_github_repository(self, page):
        """Test GitHub repository page"""
        print("\n🔍 Testing GitHub Repository...")
        
        try:
            await page.goto(self.repo_url, wait_until='networkidle')
            
            # Test repository title
            title = await page.title()
            if "agents" in title.lower() and "minuetai" in title.lower():
                self.log_result("Repository Title", True, f"'{title}'")
            else:
                self.log_result("Repository Title", False, f"Unexpected title: '{title}'")
            
            # Test repository description - try multiple selectors
            description = None
            description_selectors = [
                "[data-pjax='#repo-content-pjax-container'] p",
                ".repository-meta .f4",
                "#repo-content-pjax-container p", 
                "p.f4.my-3"
            ]
            
            for selector in description_selectors:
                try:
                    desc_elem = page.locator(selector)
                    if await desc_elem.count() > 0:
                        description = await desc_elem.first.text_content()
                        if description and description.strip():
                            break
                except:
                    continue
            
            if description and "open infrastructure" in description.lower():
                self.log_result("Repository Description", True, f"'{description.strip()}'")
            else:
                self.log_result("Repository Description", False, f"Missing or incorrect: '{description}'")
            
            # Test repository website URL
            website_url = None
            website_selectors = [
                "a[href*='minuetai.github.io']",
                "[data-testid='link-with-tooltip'] a",
                ".BorderGrid-cell a[href*='github.io']"
            ]
            
            for selector in website_selectors:
                try:
                    url_elem = page.locator(selector)
                    if await url_elem.count() > 0:
                        website_url = await url_elem.first.get_attribute('href')
                        if website_url and 'minuetai.github.io' in website_url:
                            break
                except:
                    continue
            
            if website_url and website_url == "https://minuetai.github.io/agents/":
                self.log_result("Repository Website URL", True, f"'{website_url}'")
            else:
                self.log_result("Repository Website URL", False, f"Expected 'https://minuetai.github.io/agents/', got '{website_url}'")
            
            # Test README heading
            readme_heading = await page.locator("article h1").first.text_content()
            if readme_heading and readme_heading.strip() == "Agents":
                self.log_result("README Heading", True, f"'{readme_heading}'")
            else:
                self.log_result("README Heading", False, f"Expected 'Agents', got '{readme_heading}'")
            
            # Test README subtitle
            readme_subtitle = await page.locator("article p").first.text_content()
            if readme_subtitle and "the open infrastructure" in readme_subtitle.lower():
                self.log_result("README Subtitle", True, f"Contains authoritative positioning")
            else:
                self.log_result("README Subtitle", False, f"Missing authoritative positioning: '{readme_subtitle}'")
            
            # Test schema.json file exists
            files_link = page.locator("a[href*='schema.json']")
            if await files_link.count() > 0:
                self.log_result("schema.json File", True, "File link found")
            else:
                self.log_result("schema.json File", False, "File link not found")
            
            # Test CI badge status
            ci_badge = page.locator("img[alt*='CI'], img[alt*='build']")
            if await ci_badge.count() > 0:
                badge_src = await ci_badge.first.get_attribute('src')
                self.log_result("CI Badge", True, f"Badge present: {badge_src}")
            else:
                self.log_result("CI Badge", False, "CI badge not found")
            
            # Test example files naming - check content not just links
            page_content = await page.content()
            individual_found = "example_individual_agent.json" in page_content
            corporate_found = "example_corporate_agent.json" in page_content
            
            # Also check for old profile references that shouldn't exist
            old_individual = "example_individual_profile.json" in page_content
            old_corporate = "example_corporate_profile.json" in page_content
            
            if individual_found and corporate_found and not old_individual and not old_corporate:
                self.log_result("Example Files Naming", True, "Both *_agent.json files referenced, no old *_profile.json")
            else:
                issues = []
                if not individual_found: issues.append("missing individual_agent.json")
                if not corporate_found: issues.append("missing corporate_agent.json") 
                if old_individual: issues.append("found old individual_profile.json")
                if old_corporate: issues.append("found old corporate_profile.json")
                self.log_result("Example Files Naming", False, f"Issues: {', '.join(issues)}")
            
            # Test for old references (should not exist) - be more specific
            # (reuse page_content from above)
            old_refs_count = 0
            old_refs_list = []
            
            # Check for specific old patterns that shouldn't exist
            old_patterns = [
                "agent-profile-schema",
                "agent_profile_v1.0.json",
                "example_individual_profile.json",
                "example_corporate_profile.json"
            ]
            
            legacy_details = []
            for pattern in old_patterns:
                if pattern in page_content:
                    count = page_content.count(pattern)
                    old_refs_count += count
                    old_refs_list.append(pattern)
                    
                    # Find context around each occurrence
                    lines = page_content.split('\n')
                    for i, line in enumerate(lines):
                        if pattern in line:
                            # Get some context
                            context = line.strip()[:100] + "..." if len(line.strip()) > 100 else line.strip()
                            legacy_details.append(f"  • {pattern} in line {i+1}: {context}")
            
            if old_refs_count == 0:
                self.log_result("No Old References", True, "No legacy references found")
            else:
                details = f"Found {old_refs_count} legacy references:\n" + "\n".join(legacy_details[:10])  # Limit to first 10
                if len(legacy_details) > 10:
                    details += f"\n  ... and {len(legacy_details) - 10} more"
                self.log_result("No Old References", False, details)
                
        except Exception as e:
            self.log_result("GitHub Repository Test", False, f"Error: {str(e)}")

    async def test_github_pages(self, page):
        """Test GitHub Pages registry viewer"""
        print("\n🔍 Testing GitHub Pages...")
        
        try:
            response = await page.goto(self.pages_url, wait_until='networkidle')
            
            # Test page loads successfully
            if response.status == 200:
                self.log_result("Pages Load", True, f"Status {response.status}")
            else:
                self.log_result("Pages Load", False, f"Status {response.status}")
                return
            
            # Test page title
            title = await page.title()
            if "agent" in title.lower():
                self.log_result("Pages Title", True, f"'{title}'")
            else:
                self.log_result("Pages Title", False, f"Unexpected title: '{title}'")
            
            # Test registry functionality and data source
            table = page.locator("table")
            if await table.count() > 0:
                self.log_result("Registry Table", True, "Registry table found")
                
                # Check if the page is loading from the correct JSON source
                page_content = await page.content()
                if "agents_index.json" in page_content:
                    self.log_result("Registry Data Source", True, "Loading from agents_index.json")
                elif "profiles_index.json" in page_content:
                    self.log_result("Registry Data Source", False, "Still loading from old profiles_index.json")
                else:
                    self.log_result("Registry Data Source", False, "Cannot determine data source")
                
                # Wait for dynamic content to load and check actual agent count
                await page.wait_for_timeout(3000)  # Give time for fetch to complete
                rows = await page.locator("table tbody tr").count()
                
                # We expect 8 agents (7 examples + 1 external from cialint repo)
                expected_count = 8
                if rows == expected_count:
                    self.log_result("Registry Content Count", True, f"Correct count: {rows} agents")
                elif rows > 0:
                    self.log_result("Registry Content Count", False, f"Expected {expected_count} agents, found {rows} (possibly cached data)")
                else:
                    self.log_result("Registry Content Count", False, "No agents in registry")
                    
                # Verify we can see specific agents from our examples
                agent_names = ["MapSummarizer", "EnterpriseWebNavigator"]  # From our examples
                found_agents = []
                for agent_name in agent_names:
                    agent_cell = page.locator(f"td:has-text('{agent_name}')")
                    if await agent_cell.count() > 0:
                        found_agents.append(agent_name)
                
                if len(found_agents) == len(agent_names):
                    self.log_result("Registry Example Agents", True, f"Found expected agents: {', '.join(found_agents)}")
                else:
                    self.log_result("Registry Example Agents", False, f"Missing agents. Found: {found_agents}, Expected: {agent_names}")
                    
            else:
                self.log_result("Registry Table", False, "Registry table not found")
                
        except Exception as e:
            self.log_result("GitHub Pages Test", False, f"Error: {str(e)}")

    async def test_schema_validation(self, page):
        """Test schema file accessibility and basic structure"""
        print("\n🔍 Testing Schema File...")
        
        try:
            # Try raw GitHub URL first, then GitHub Pages
            schema_urls = [
                "https://raw.githubusercontent.com/minuetai/agents/main/schema.json",
                f"{self.pages_url}schema.json"
            ]
            
            response = None
            for schema_url in schema_urls:
                try:
                    response = await page.goto(schema_url)
                    if response.status == 200:
                        break
                except:
                    continue
            
            if response and response.status == 200:
                self.log_result("Schema File Access", True, f"Status {response.status}")
                
                # Get schema content
                content = await page.content()
                
                # Basic JSON structure checks
                if '"title": "Minuet Agent Schema"' in content:
                    self.log_result("Schema Title", True, "Correct schema title")
                else:
                    self.log_result("Schema Title", False, "Incorrect or missing schema title")
                
                if '"$id": "https://minuetai.github.io/agents/schema.json"' in content:
                    self.log_result("Schema $id", True, "Correct schema $id")
                else:
                    self.log_result("Schema $id", False, "Incorrect or missing schema $id")
                
                if '"description": "The canonical open schema' in content:
                    self.log_result("Schema Description", True, "Authoritative description")
                else:
                    self.log_result("Schema Description", False, "Missing authoritative description")
                    
            else:
                status = response.status if response else "No response"
                self.log_result("Schema File Access", False, f"Status {status}")
                
        except Exception as e:
            self.log_result("Schema File Test", False, f"Error: {str(e)}")

    async def test_example_files(self, page):
        """Test example files accessibility"""
        print("\n🔍 Testing Example Files...")
        
        example_files = [
            "example_individual_agent.json",
            "example_corporate_agent.json", 
            "example_enterprise_v1.0.json"
        ]
        
        for filename in example_files:
            try:
                file_url = f"https://raw.githubusercontent.com/minuetai/agents/main/examples/{filename}"
                response = await page.goto(file_url)
                
                if response.status == 200:
                    self.log_result(f"Example: {filename}", True, "Accessible")
                else:
                    self.log_result(f"Example: {filename}", False, f"Status {response.status}")
                    
            except Exception as e:
                self.log_result(f"Example: {filename}", False, f"Error: {str(e)}")

    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🚀 Starting Repository Health Check...")
        print(f"Repository: {self.repo_url}")
        print(f"GitHub Pages: {self.pages_url}")
        
        async with async_playwright() as p:
            # Use chromium for testing
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (compatible; RepoHealthChecker/1.0)"
            )
            page = await context.new_page()
            
            # Run all test suites
            await self.test_github_repository(page)
            await self.test_github_pages(page)
            await self.test_schema_validation(page)
            await self.test_example_files(page)
            
            await browser.close()
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        for result in self.results:
            print(result)
        
        print("\n" + "="*60)
        if self.failed:
            print("❌ SOME TESTS FAILED - Review issues above")
            return 1
        else:
            print("✅ ALL TESTS PASSED - Repository looks healthy!")
            return 0

async def main():
    checker = RepoHealthChecker()
    exit_code = await checker.run_all_tests()
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error: {e}")
        sys.exit(1)