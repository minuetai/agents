#!/usr/bin/env python3
"""
Analyze agent discovery findings to quickly identify the most relevant items
"""

import json
from pathlib import Path
from collections import Counter
import re

def analyze_findings(json_file):
    with open(json_file) as f:
        data = json.load(f)
    
    findings = data['findings']
    
    print("🔍 AGENT DISCOVERY ANALYSIS")
    print("=" * 50)
    
    # 1. High-impact GitHub repos (high stars + recent activity)
    print("\n📈 HIGH-IMPACT GITHUB REPOS (>1000 stars):")
    github_findings = [f for f in findings if f['source'] == 'github']
    high_impact = [f for f in github_findings if f['stars'] > 1000]
    high_impact.sort(key=lambda x: x['stars'], reverse=True)
    
    for f in high_impact[:10]:
        print(f"⭐ {f['stars']:,} - {f['title']}")
        print(f"   {f['description'][:80]}...")
        print(f"   Topics: {', '.join(f['topics'][:5])}")
        print()
    
    # 2. Identify patterns in topics/technologies
    print("\n🏷️  TRENDING TOPICS/TECHNOLOGIES:")
    all_topics = []
    for f in github_findings:
        all_topics.extend(f.get('topics', []))
    
    topic_counts = Counter(all_topics)
    top_topics = topic_counts.most_common(15)
    
    for topic, count in top_topics:
        if topic not in ['ai', 'python', 'typescript', 'javascript']:  # Skip generic ones
            print(f"   {topic}: {count} repos")
    
    # 3. Novel/emerging patterns
    print("\n🆕 POTENTIALLY NOVEL CONCEPTS:")
    novel_keywords = [
        'mcp', 'model-context-protocol', 'agentic', 'multi-agent', 
        'agent-framework', 'agent-orchestration', 'swarm'
    ]
    
    for keyword in novel_keywords:
        matches = []
        for f in findings:
            text = f"{f['title']} {f['description']} {' '.join(f.get('topics', []))}".lower()
            if keyword in text:
                matches.append(f)
        
        if matches:
            print(f"\n   '{keyword}' - {len(matches)} matches:")
            for m in matches[:3]:  # Show top 3
                source_icon = "📁" if m['source'] == 'github' else "📄"
                stars = f"⭐{m['stars']}" if m['source'] == 'github' else ""
                print(f"     {source_icon} {m['title']} {stars}")
    
    # 4. ArXiv papers - academic trends
    print("\n📄 RECENT ACADEMIC PAPERS:")
    arxiv_findings = [f for f in findings if f['source'] == 'arxiv']
    
    for f in arxiv_findings[:5]:
        print(f"   📄 {f['title']}")
        print(f"      {f['description'][:100]}...")
        print()
    
    # 5. Quick relevance scoring
    print("\n🎯 QUICK RELEVANCE ASSESSMENT:")
    
    # Score based on multiple factors
    scored_findings = []
    for f in findings:
        score = 0
        text = f"{f['title']} {f['description']}".lower()
        
        # High-value keywords
        if any(kw in text for kw in ['agent profile', 'agent discovery', 'agent registry']):
            score += 10
        if any(kw in text for kw in ['agent framework', 'multi-agent', 'agent orchestration']):
            score += 5
        if any(kw in text for kw in ['llm agent', 'ai agent', 'autonomous agent']):
            score += 3
        
        # GitHub-specific scoring
        if f['source'] == 'github':
            if f['stars'] > 5000:
                score += 5
            elif f['stars'] > 1000:
                score += 3
            elif f['stars'] > 100:
                score += 1
                
        # Penalize if too generic
        if any(kw in text for kw in ['tutorial', 'example', 'demo', 'hello world']):
            score -= 2
            
        if score > 0:
            scored_findings.append((score, f))
    
    scored_findings.sort(reverse=True)
    
    print("   TOP 5 BY RELEVANCE SCORE:")
    for score, f in scored_findings[:5]:
        source_icon = "📁" if f['source'] == 'github' else "📄"
        stars = f"⭐{f['stars']}" if f['source'] == 'github' else ""
        print(f"   [{score}] {source_icon} {f['title']} {stars}")
        print(f"       {f['description'][:80]}...")
        print()
    
    # 6. Action recommendations
    print("\n💡 RECOMMENDED ACTIONS:")
    
    # Find potential schema additions
    schema_relevant = [f for score, f in scored_findings if score >= 7]
    if schema_relevant:
        print(f"   🔧 SCHEMA UPDATES: Review {len(schema_relevant)} high-scoring items for schema additions")
    
    # Find potential example additions
    example_candidates = [f for f in github_findings if f['stars'] > 500 and 'agent' in f['title'].lower()]
    if example_candidates:
        print(f"   📝 NEW EXAMPLES: Consider {len(example_candidates)} repos for example profiles")
    
    # Find ecosystem trends
    trending_topics = [topic for topic, count in top_topics[:5] if count >= 3]
    if trending_topics:
        print(f"   📈 TRENDING: Monitor these topics: {', '.join(trending_topics)}")
    
    print(f"\n✅ Analysis complete! Reviewed {len(findings)} findings.")

if __name__ == '__main__':
    # Find the most recent findings file
    output_dir = Path('discovery_output')
    json_files = list(output_dir.glob('agent_findings_*.json'))
    
    if not json_files:
        print("No findings files found!")
        exit(1)
    
    latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
    print(f"Analyzing: {latest_file}")
    
    analyze_findings(latest_file)