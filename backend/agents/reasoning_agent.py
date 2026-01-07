import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any

class ReasoningAgent:
    def __init__(self):
        # Global political analysis keywords
        self.political_keywords = {
            'positive': ['passed', 'signed', 'approved', 'successful', 'achieved', 'delivered', 'completed', 'won', 'elected', 'implemented'],
            'negative': ['failed', 'rejected', 'vetoed', 'blocked', 'unsuccessful', 'delayed', 'cancelled', 'defeated', 'resigned', 'scandal'],
            'neutral': ['proposed', 'introduced', 'discussed', 'reviewed', 'considered', 'pending', 'announced', 'stated']
        }
        
        # Global political positions
        self.global_positions = {
            'president': ['president', 'prime minister', 'chancellor', 'premier'],
            'legislature': ['senator', 'mp', 'member of parliament', 'representative', 'deputy', 'congressman'],
            'regional': ['governor', 'mayor', 'minister', 'chief minister', 'first minister'],
            'party': ['party leader', 'opposition leader', 'secretary general']
        }
        
        # Global political parties and ideologies
        self.political_spectrum = {
            'left': ['labour', 'social democratic', 'socialist', 'communist', 'green', 'progressive'],
            'center': ['liberal', 'centrist', 'moderate', 'independent'],
            'right': ['conservative', 'republican', 'nationalist', 'christian democratic']
        }

    async def analyze(self, name: str, raw_data: Dict) -> Dict[str, Any]:
        """Main analysis method that processes real fetched data using internal reasoning"""
        
        # Extract real data from APIs
        wiki_data = raw_data.get('wikipedia', {})
        news_data = raw_data.get('news', [])
        
        # Analyze real data using internal reasoning
        basic_info = self._extract_basic_info(name, wiki_data)
        activities = self._analyze_real_activities(name, wiki_data, news_data)
        promises = self._extract_real_promises(name, wiki_data, news_data)
        bills = self._extract_real_legislative_record(name, wiki_data, activities)
        voting_record = self._analyze_real_voting_patterns(name, wiki_data)
        controversies = self._identify_real_controversies(name, wiki_data, news_data)
        promise_analysis = self._calculate_promise_metrics(promises)
        
        return {
            "politician": name,
            "party": basic_info.get('party', 'Unknown'),
            "position": basic_info.get('position', 'Political Figure'),
            "term_period": basic_info.get('term_period', 'N/A'),
            "summary": basic_info.get('summary', f"{name} is a political figure."),
            "activities": activities,
            "promises": promises,
            "bills": bills,
            "promise_analysis": promise_analysis,
            "voting_record_summary": voting_record,
            "controversies": controversies,
            "data_sources": ["Wikipedia API", "NewsAPI", "Internal Global Political Analysis Engine"]
        }

    def _extract_basic_info(self, name: str, wiki_data: Dict) -> Dict[str, str]:
        """Extract basic politician information from real Wikipedia data"""
        extract = wiki_data.get('extract', '').lower()
        title = wiki_data.get('title', name)
        
        # Determine party affiliation globally
        party = self._identify_political_party(extract)
        
        # Determine position globally
        position = self._identify_political_position(extract, name)
        
        # Extract term period using pattern matching
        term_period = self._extract_term_period(extract)
        
        return {
            'party': party,
            'position': position,
            'term_period': term_period,
            'summary': self._generate_contextual_summary(name, party, position, extract)
        }

    def _identify_political_party(self, text: str) -> str:
        """Identify political party from text using global patterns"""
        # Look for explicit party mentions
        party_patterns = [
            r'member of the ([^,\.]+party)',
            r'([^,\.]+party) member',
            r'represents the ([^,\.]+party)',
            r'leader of the ([^,\.]+party)'
        ]
        
        for pattern in party_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).title()
        
        # Classify by political spectrum
        for spectrum, keywords in self.political_spectrum.items():
            if any(keyword in text for keyword in keywords):
                return f"{spectrum.title()} Political Party"
        
        return 'Unknown'

    def _identify_political_position(self, text: str, name: str) -> str:
        """Identify political position from text globally"""
        text_lower = text.lower()
        
        # Check for executive positions
        for pos_type, keywords in self.global_positions.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if pos_type == 'president':
                        if 'former' in text_lower or 'was' in text_lower:
                            return f"Former {keyword.title()}"
                        return keyword.title()
                    else:
                        return keyword.title()
        
        # Look for country-specific titles
        country_titles = {
            'india': ['prime minister', 'chief minister', 'mp'],
            'uk': ['prime minister', 'mp', 'lord'],
            'germany': ['chancellor', 'minister'],
            'france': ['president', 'prime minister'],
            'canada': ['prime minister', 'mp']
        }
        
        for country, titles in country_titles.items():
            if country in text_lower:
                for title in titles:
                    if title in text_lower:
                        return title.title()
        
        return 'Political Figure'

    def _extract_term_period(self, text: str) -> str:
        """Extract term period from text"""
        # Look for year ranges
        year_patterns = [
            r'(\d{4})\s*[-–]\s*(\d{4})',
            r'(\d{4})\s*[-–]\s*present',
            r'since\s*(\d{4})'
        ]
        
        for pattern in year_patterns:
            match = re.search(pattern, text)
            if match:
                if len(match.groups()) == 2:
                    return f"{match.group(1)}-{match.group(2)}"
                else:
                    return f"{match.group(1)}-present"
        
        return 'N/A'

    def _generate_contextual_summary(self, name: str, party: str, position: str, extract: str) -> str:
        """Generate summary based on real data analysis"""
        # Extract key achievements or focus areas from the text
        focus_areas = []
        if 'economic' in extract or 'economy' in extract:
            focus_areas.append('economic policy')
        if 'health' in extract or 'healthcare' in extract:
            focus_areas.append('healthcare')
        if 'environment' in extract or 'climate' in extract:
            focus_areas.append('environmental issues')
        if 'education' in extract:
            focus_areas.append('education')
        
        focus_text = f", focusing on {', '.join(focus_areas)}" if focus_areas else ""
        
        return f"{name} serves as {position} representing {party}{focus_text}."

    def _analyze_real_activities(self, name: str, wiki_data: Dict, news_data: List) -> List[Dict]:
        """Analyze real activities from fetched news data"""
        activities = []
        
        # Process real news articles
        for article in news_data[:6]:  # Limit to recent articles
            title = article.get('title', '')
            description = article.get('description', '')
            published_at = article.get('publishedAt', '')
            
            if title and name.lower() in title.lower():
                activity = {
                    'activity': title,
                    'date': self._parse_news_date(published_at),
                    'category': self._classify_activity_category(title, description),
                    'impact': self._assess_activity_impact(title, description),
                    'details': description or 'No additional details available.'
                }
                activities.append(activity)
        
        # If no news activities, extract from Wikipedia
        if not activities:
            activities = self._extract_wiki_activities(name, wiki_data)
        
        return activities[:6]

    def _parse_news_date(self, date_str: str) -> str:
        """Parse news date to readable format"""
        try:
            if date_str:
                date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                return date_obj.strftime('%Y-%m')
        except:
            pass
        return datetime.now().strftime('%Y-%m')

    def _classify_activity_category(self, title: str, description: str) -> str:
        """Classify activity category from real content"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ['bill', 'law', 'legislation', 'vote', 'parliament', 'congress']):
            return 'Legislation'
        elif any(word in text for word in ['campaign', 'election', 'rally', 'candidate']):
            return 'Campaign'
        elif any(word in text for word in ['meeting', 'summit', 'visit', 'diplomatic', 'foreign']):
            return 'Diplomacy'
        elif any(word in text for word in ['statement', 'speech', 'address', 'comment']):
            return 'Public Statement'
        elif any(word in text for word in ['policy', 'reform', 'initiative']):
            return 'Policy Initiative'
        else:
            return 'General Activity'

    def _assess_activity_impact(self, title: str, description: str) -> str:
        """Assess activity impact from content"""
        text = f"{title} {description}".lower()
        
        positive_count = sum(1 for word in self.political_keywords['positive'] if word in text)
        negative_count = sum(1 for word in self.political_keywords['negative'] if word in text)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'controversial'
        else:
            return 'neutral'

    def _extract_wiki_activities(self, name: str, wiki_data: Dict) -> List[Dict]:
        """Extract activities from Wikipedia content when no news available"""
        extract = wiki_data.get('extract', '')
        
        # Look for recent activities in the text
        activities = []
        sentences = extract.split('. ')
        
        for sentence in sentences[-3:]:  # Last few sentences often contain recent info
            if any(word in sentence.lower() for word in ['recent', '2024', '2023', 'current']):
                activities.append({
                    'activity': sentence.strip(),
                    'date': '2024',
                    'category': 'General Activity',
                    'impact': 'neutral',
                    'details': 'Extracted from biographical information'
                })
        
        return activities

    def _extract_real_promises(self, name: str, wiki_data: Dict, news_data: List) -> List[Dict]:
        """Extract real promises from fetched data instead of generating fake ones"""
        promises = []
        extract = wiki_data.get('extract', '').lower()
        
        # Look for promise-related keywords in Wikipedia
        promise_sentences = []
        for sentence in extract.split('.'):
            if any(word in sentence.lower() for word in ['promise', 'pledge', 'commit', 'plan to', 'will', 'intend']):
                promise_sentences.append(sentence.strip())
        
        # Extract promises from news articles
        for article in news_data:
            title = article.get('title', '')
            description = article.get('description', '')
            
            if any(word in f"{title} {description}".lower() for word in ['promise', 'pledge', 'commit', 'plan']):
                promises.append({
                    'promise': title,
                    'made_during': 'Recent statements',
                    'evidence': description,
                    'timeline': 'Ongoing',
                    'impact': 'To be determined based on implementation'
                })
        
        # Convert Wikipedia sentences to promises
        for sentence in promise_sentences[:3]:
            promises.append({
                'promise': sentence,
                'made_during': 'Political career',
                'evidence': 'Mentioned in biographical information',
                'timeline': 'Ongoing',
                'impact': 'Policy-related commitment'
            })
        
        # Calculate fulfillment for each promise
        for promise in promises:
            promise['fulfillment_percentage'] = self._calculate_real_fulfillment(promise, wiki_data, news_data)
            promise['status'] = self._determine_promise_status(promise['fulfillment_percentage'])
        
        return promises[:6]

    def _calculate_real_fulfillment(self, promise: Dict, wiki_data: Dict, news_data: List) -> int:
        """Calculate promise fulfillment based on real data analysis"""
        promise_text = promise['promise'].lower()
        fulfillment_score = 0
        
        # Check Wikipedia for fulfillment evidence
        wiki_text = wiki_data.get('extract', '').lower()
        if any(word in wiki_text for word in ['achieved', 'completed', 'implemented', 'delivered']):
            fulfillment_score += 40
        
        # Check news for recent progress
        for article in news_data:
            article_text = f"{article.get('title', '')} {article.get('description', '')}".lower()
            
            # Look for progress indicators
            if any(word in article_text for word in promise_text.split()[:3]):  # Key words from promise
                if any(word in article_text for word in ['progress', 'working', 'developing']):
                    fulfillment_score += 20
                elif any(word in article_text for word in ['completed', 'achieved', 'delivered']):
                    fulfillment_score += 50
        
        return min(fulfillment_score, 100)

    def _extract_real_legislative_record(self, name: str, wiki_data: Dict, activities: List) -> List[Dict]:
        """Extract real legislative information from data"""
        bills = []
        extract = wiki_data.get('extract', '').lower()
        
        # Look for legislative mentions in Wikipedia
        legislative_keywords = ['bill', 'act', 'law', 'legislation', 'reform']
        sentences = extract.split('.')
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in legislative_keywords):
                # Extract potential bill names
                bill_match = re.search(r'([A-Z][^.]*(?:act|bill|law))', sentence, re.IGNORECASE)
                if bill_match:
                    bill_name = bill_match.group(1).strip()
                    bills.append({
                        'title': bill_name,
                        'bill_number': 'N/A',
                        'year': self._extract_year_from_text(sentence),
                        'description': sentence.strip(),
                        'status': self._determine_bill_status(sentence),
                        'role': self._determine_legislative_role(sentence, name),
                        'impact_area': self._determine_policy_area(sentence)
                    })
        
        # Extract from activities
        for activity in activities:
            if activity['category'] == 'Legislation':
                bills.append({
                    'title': activity['activity'],
                    'bill_number': 'N/A',
                    'year': activity['date'][:4] if activity['date'] else '2024',
                    'description': activity['details'],
                    'status': 'Recent Activity',
                    'role': 'Involved',
                    'impact_area': self._determine_policy_area(activity['activity'])
                })
        
        return bills[:5]

    def _extract_year_from_text(self, text: str) -> str:
        """Extract year from text"""
        year_match = re.search(r'(19|20)\d{2}', text)
        return year_match.group(0) if year_match else '2024'

    def _determine_bill_status(self, text: str) -> str:
        """Determine bill status from context"""
        text = text.lower()
        if any(word in text for word in ['passed', 'enacted', 'signed']):
            return 'Passed'
        elif any(word in text for word in ['proposed', 'introduced']):
            return 'Introduced'
        elif any(word in text for word in ['failed', 'rejected']):
            return 'Failed'
        else:
            return 'Unknown'

    def _determine_legislative_role(self, text: str, name: str) -> str:
        """Determine politician's role in legislation"""
        text = text.lower()
        name_lower = name.lower()
        
        if any(word in text for word in [f'{name_lower} introduced', f'{name_lower} proposed']):
            return 'Sponsor'
        elif any(word in text for word in [f'{name_lower} supported', f'{name_lower} backed']):
            return 'Supporter'
        elif any(word in text for word in [f'{name_lower} voted', f'{name_lower} opposed']):
            return 'Voter'
        else:
            return 'Involved'

    def _analyze_real_voting_patterns(self, name: str, wiki_data: Dict) -> Dict:
        """Analyze real voting patterns from data"""
        extract = wiki_data.get('extract', '').lower()
        
        # Determine political alignment from real data
        alignment = 'moderate'
        for spectrum, keywords in self.political_spectrum.items():
            if any(keyword in extract for keyword in keywords):
                alignment = spectrum
                break
        
        # Extract real voting information
        key_votes = []
        vote_sentences = [s for s in extract.split('.') if 'vote' in s.lower() or 'support' in s.lower()]
        
        for sentence in vote_sentences[:3]:
            issue_match = re.search(r'(vote[d]?|support[ed]?)\s+([^.]+)', sentence, re.IGNORECASE)
            if issue_match:
                key_votes.append({
                    'issue': issue_match.group(2).strip(),
                    'position': 'For' if 'support' in sentence.lower() else 'Voted',
                    'year': self._extract_year_from_text(sentence)
                })
        
        return {
            'key_votes': key_votes,
            'alignment': alignment
        }

    def _identify_real_controversies(self, name: str, wiki_data: Dict, news_data: List) -> List[Dict]:
        """Identify real controversies from fetched data"""
        controversies = []
        
        # Check news for controversial content
        controversy_keywords = ['controversy', 'scandal', 'criticism', 'dispute', 'allegation', 'investigation']
        
        for article in news_data:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            
            if any(keyword in f"{title} {description}" for keyword in controversy_keywords):
                controversies.append({
                    'issue': article.get('title', 'Political controversy'),
                    'year': self._parse_news_date(article.get('publishedAt', ''))[:4],
                    'resolution': 'Ongoing news coverage'
                })
        
        # Check Wikipedia for historical controversies
        extract = wiki_data.get('extract', '').lower()
        for keyword in controversy_keywords:
            if keyword in extract:
                sentences = [s for s in extract.split('.') if keyword in s.lower()]
                for sentence in sentences[:2]:
                    controversies.append({
                        'issue': sentence.strip(),
                        'year': self._extract_year_from_text(sentence),
                        'resolution': 'Historical record'
                    })
        
        return controversies[:3]

    def _determine_promise_status(self, percentage: int) -> str:
        """Determine promise status based on fulfillment percentage"""
        if percentage >= 80:
            return 'fulfilled'
        elif percentage >= 60:
            return 'partially_fulfilled'
        elif percentage >= 30:
            return 'in_progress'
        else:
            return 'not_fulfilled'

    def _determine_policy_area(self, text: str) -> str:
        """Determine policy area from text globally"""
        text = text.lower()
        if any(word in text for word in ['health', 'medical', 'care', 'hospital', 'medicine']):
            return 'Healthcare'
        elif any(word in text for word in ['economy', 'job', 'business', 'trade', 'finance', 'economic']):
            return 'Economy'
        elif any(word in text for word in ['environment', 'climate', 'energy', 'green', 'carbon']):
            return 'Environment'
        elif any(word in text for word in ['defense', 'military', 'security', 'army', 'war']):
            return 'Defense'
        elif any(word in text for word in ['education', 'school', 'university', 'student']):
            return 'Education'
        elif any(word in text for word in ['infrastructure', 'transport', 'road', 'bridge']):
            return 'Infrastructure'
        elif any(word in text for word in ['social', 'welfare', 'pension', 'benefit']):
            return 'Social Policy'
        else:
            return 'General Policy'

    def _calculate_promise_metrics(self, promises: List[Dict]) -> Dict:
        """Calculate comprehensive promise fulfillment metrics"""
        if not promises:
            return {}
        
        total = len(promises)
        fulfilled = sum(1 for p in promises if p.get('status') == 'fulfilled')
        partially = sum(1 for p in promises if p.get('status') == 'partially_fulfilled')
        in_progress = sum(1 for p in promises if p.get('status') == 'in_progress')
        not_fulfilled = sum(1 for p in promises if p.get('status') == 'not_fulfilled')
        
        fulfillment_rate = round(((fulfilled + 0.5 * partially) / total) * 100, 1) if total > 0 else 0
        
        return {
            'total_promises_tracked': total,
            'fulfilled_count': fulfilled,
            'partially_fulfilled_count': partially,
            'in_progress_count': in_progress,
            'not_fulfilled_count': not_fulfilled,
            'calculated_fulfillment_rate': f"{fulfillment_rate}%",
            'strongest_areas': self._identify_strong_areas(promises),
            'weakest_areas': self._identify_weak_areas(promises),
            'analysis_summary': f"Based on available data, promise fulfillment rate of {fulfillment_rate}% indicates {'strong' if fulfillment_rate > 60 else 'moderate' if fulfillment_rate > 30 else 'developing'} progress on stated commitments."
        }

    def _identify_strong_areas(self, promises: List[Dict]) -> List[str]:
        """Identify areas where promises are being fulfilled"""
        strong_areas = []
        for promise in promises:
            if promise.get('status') in ['fulfilled', 'partially_fulfilled']:
                # Extract policy area from promise text
                area = self._determine_policy_area(promise.get('promise', ''))
                if area not in strong_areas and area != 'General Policy':
                    strong_areas.append(area)
        return strong_areas[:3]

    def _identify_weak_areas(self, promises: List[Dict]) -> List[str]:
        """Identify areas where promises are not being fulfilled"""
        weak_areas = []
        for promise in promises:
            if promise.get('status') == 'not_fulfilled':
                area = self._determine_policy_area(promise.get('promise', ''))
                if area not in weak_areas and area != 'General Policy':
                    weak_areas.append(area)
        return weak_areas[:3]