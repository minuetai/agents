#!/usr/bin/env python3
"""
Agent Discovery Script

Monitors various sources for new agent-related developments:
- GitHub repositories with agent topics
- arXiv papers about agents
- RSS feeds from key AI sources

Saves findings to JSON files for manual review before incorporation.
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

class AgentDiscovery:
    def __init__(self):
        self.findings = []
        self.config = {
            'github_topics': ['ai-agent', 'autonomous-agent', 'llm-agent', 'agent-profile'],
            'days_back': 7,  # Look for items from last N days
            'output_dir': Path(__file__).parent / 'discovery_output'
        }
        
        # Create output directory
        self.config['output_dir'].mkdir(exist_ok=True)
    
    def scan_github_topics(self):
        """Scan GitHub for recently updated repositories with agent topics"""
        print("🔍 Scanning GitHub topics...")
        
        since_date = (datetime.now() - timedelta(days=self.config['days_back'])).strftime('%Y-%m-%d')
        
        for topic in self.config['github_topics']:
            try:
                # Search for repositories with the topic, updated recently
                url = f"https://api.github.com/search/repositories"
                params = {
                    'q': f'topic:{topic} pushed:>{since_date}',
                    'sort': 'updated',
                    'order': 'desc',
                    'per_page': 20
                }
                
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                for repo in data.get('items', []):
                    # Skip our own repo
                    if 'cialint' in repo['full_name']:
                        continue
                        
                    finding = {
                        'source': 'github',
                        'type': 'repository',
                        'topic': topic,
                        'title': repo['name'],
                        'description': repo.get('description', ''),
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'language': repo.get('language'),
                        'updated_at': repo['updated_at'],
                        'topics': repo.get('topics', []),
                        'found_at': datetime.now().isoformat()
                    }
                    
                    # Simple relevance filtering
                    if self._is_relevant_repo(finding):
                        self.findings.append(finding)
                        
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Error scanning topic {topic}: {e}")
        
        print(f"   Found {len([f for f in self.findings if f['source'] == 'github'])} GitHub repositories")
    
    def scan_arxiv(self):
        """Scan arXiv for recent agent-related papers"""
        print("📄 Scanning arXiv papers...")
        
        try:
            # arXiv API query for recent papers with "agent" in title/abstract
            base_url = "http://export.arxiv.org/api/query"
            
            # Search in AI, ML, and CL categories for papers mentioning agents
            query = 'cat:cs.AI OR cat:cs.LG OR cat:cs.CL AND (ti:agent OR abs:agent OR ti:"large language model" OR abs:"autonomous agent")'
            
            params = {
                'search_query': query,
                'start': 0,
                'max_results': 20,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            # Parse the Atom XML response
            import xml.etree.ElementTree as ET
            root = ET.fromstring(response.content)
            
            # Extract entries
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            
            for entry in root.findall('atom:entry', namespace):
                title = entry.find('atom:title', namespace).text.strip()
                summary = entry.find('atom:summary', namespace).text.strip()
                published = entry.find('atom:published', namespace).text
                link = entry.find('atom:id', namespace).text
                
                # Check if it's from the last week and relevant
                pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                if pub_date < datetime.now().replace(tzinfo=pub_date.tzinfo) - timedelta(days=self.config['days_back']):
                    continue
                
                finding = {
                    'source': 'arxiv',
                    'type': 'paper',
                    'title': title,
                    'description': summary[:500] + '...' if len(summary) > 500 else summary,
                    'url': link.replace('http://arxiv.org/abs/', 'https://arxiv.org/abs/'),
                    'published_at': published,
                    'found_at': datetime.now().isoformat()
                }
                
                if self._is_relevant_paper(finding):
                    self.findings.append(finding)
                    
        except Exception as e:
            print(f"⚠️  Error scanning arXiv: {e}")
        
        print(f"   Found {len([f for f in self.findings if f['source'] == 'arxiv'])} arXiv papers")
    
    def _is_relevant_repo(self, finding):
        """Filter for relevant repositories"""
        # Skip low-quality repos
        if finding['stars'] < 5:
            return False
            
        # Look for agent-related keywords
        text = f"{finding['title']} {finding['description']}".lower()
        
        relevant_keywords = [
            'agent', 'autonomous', 'llm', 'language model', 
            'assistant', 'chatbot', 'ai agent', 'multi-agent'
        ]
        
        return any(keyword in text for keyword in relevant_keywords)
    
    def _is_relevant_paper(self, finding):
        """Filter for relevant papers"""
        text = f"{finding['title']} {finding['description']}".lower()
        
        # Must mention agents prominently
        agent_terms = ['agent', 'autonomous', 'multi-agent', 'agent-based']
        if not any(term in text for term in agent_terms):
            return False
            
        # Exclude pure theory papers, focus on applied/systems work
        exclude_terms = ['theorem', 'proof', 'mathematical', 'theoretical analysis']
        if any(term in text for term in exclude_terms):
            return False
            
        return True
    
    def save_findings(self):
        """Save all findings to timestamped JSON file"""
        if not self.findings:
            print("📭 No new findings to save")
            return
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = self.config['output_dir'] / f'agent_findings_{timestamp}.json'
        
        # Sort by source and relevance
        self.findings.sort(key=lambda x: (x['source'], x.get('stars', 0)), reverse=True)
        
        with open(filename, 'w') as f:
            json.dump({
                'scan_date': datetime.now().isoformat(),
                'total_findings': len(self.findings),
                'sources': list(set(f['source'] for f in self.findings)),
                'findings': self.findings
            }, f, indent=2)
        
        print(f"💾 Saved {len(self.findings)} findings to {filename}")
        
        # Print summary
        by_source = {}
        for finding in self.findings:
            source = finding['source']
            by_source[source] = by_source.get(source, 0) + 1
            
        print("📊 Summary:")
        for source, count in by_source.items():
            print(f"   {source}: {count} items")
    
    def run(self):
        """Run the full discovery process"""
        print("🚀 Starting agent discovery scan...")
        print(f"   Looking back {self.config['days_back']} days")
        
        self.scan_github_topics()
        self.scan_arxiv()
        self.save_findings()
        
        print("✅ Discovery scan complete!")

if __name__ == '__main__':
    discovery = AgentDiscovery()
    discovery.run()