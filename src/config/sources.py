from typing import Dict, Any, Optional
from pydantic import BaseModel
import tldextract

class SourceMetadata(BaseModel):
    name: str
    ownership: str
    funding: str
    ideological_lean: str # Left, Center-Left, Center, Center-Right, Right
    notes: Optional[str] = None

# A foundational "Source Knowledge Base" for Indian Media
# Keys are 'registered_domain' (domain.suffix) for robust matching
SOURCE_KB: Dict[str, SourceMetadata] = {
    "google.com": SourceMetadata(
        name="Google News",
        ownership="Alphabet Inc.",
        funding="Advertising",
        ideological_lean="Center",
        notes="Aggregator that surface stories from multiple publishers."
    ),
    "aninews.in": SourceMetadata(
        name="ANI (Asian News International)",
        ownership="Prem Prakash / Sanjiv Prakash",
        funding="Wire Subscription Services",
        ideological_lean="Right / Nationalist",
        notes="India's leading multimedia news agency; often criticized for a pro-government stance."
    ),
    "ptinews.com": SourceMetadata(
        name="PTI (Press Trust of India)",
        ownership="Non-profit Co-operative of Indian Newspapers",
        funding="Subscription Services",
        ideological_lean="Center",
        notes="India's largest news agency; maintained a reputation for neutral, factual wire reporting."
    ),
    "thehindu.com": SourceMetadata(
        name="The Hindu",
        ownership="Kasturi & Sons Ltd (Family-owned)",
        funding="Advertising & Subscriptions",
        ideological_lean="Center-Left",
        notes="Known for traditional, sober reporting; often critical of government policy."
    ),
    "ndtv.com": SourceMetadata(
        name="NDTV",
        ownership="AMG Media Networks (Adani Group)",
        funding="Corporate-owned",
        ideological_lean="Center to Center-Right",
        notes="Shifted from Center-Left to Center/Center-Right after Adani acquisition."
    ),
    "republicworld.com": SourceMetadata(
        name="Republic TV",
        ownership="Arnab Goswami (Arg Outlier Media)",
        funding="Advertising",
        ideological_lean="Right",
        notes="Known for high-decibel, nationalist framing; strongly pro-government."
    ),
    "indianexpress.com": SourceMetadata(
        name="The Indian Express",
        ownership="Viveck Goenka (Indian Express Group)",
        funding="Advertising & Subscriptions",
        ideological_lean="Center",
        notes="Strong focus on investigative journalism; maintains a 'neutral' but critical stance."
    ),
    "hindustantimes.com": SourceMetadata(
        name="Hindustan Times",
        ownership="Shobhana Bhartia (KK Birla Group)",
        funding="Advertising & Corporate",
        ideological_lean="Center-Right",
        notes="One of India's oldest English dailies; generally follows a pragmatic approach."
    ),
    "indiatoday.in": SourceMetadata(
        name="India Today",
        ownership="Living Media India Limited (Aroon Purie)",
        funding="Advertising",
        ideological_lean="Center-Right",
        notes="Major media group; generally takes a mainstream, pro-establishment but professional stance."
    ),
    "zeenews.india.com": SourceMetadata(
        name="Zee News",
        ownership="Essel Group (Subhash Chandra)",
        funding="Advertising",
        ideological_lean="Right",
        notes="Historically pro-nationalist and often aligned with the ruling party's narratives."
    ),
    "abplive.com": SourceMetadata(
        name="ABP News",
        ownership="ABP Group (Sarkar Family)",
        funding="Advertising",
        ideological_lean="Center-Left to Center",
        notes="Major North-Indian news broadcaster."
    ),
    "deccanherald.com": SourceMetadata(
        name="Deccan Herald",
        ownership="The Printers (Mysore) Private Limited",
        funding="Advertising",
        ideological_lean="Center",
        notes="Major Southern daily known for independence."
    ),
    "livemint.com": SourceMetadata(
        name="Livemint",
        ownership="HT Media Ltd (Birla Group)",
        funding="Advertising",
        ideological_lean="Center-Right",
        notes="Business focus with pro-market framing."
    ),
    "news18.com": SourceMetadata(
        name="News18",
        ownership="Network18 Group (Reliance Industries Ltd)",
        funding="Corporate-owned",
        ideological_lean="Right",
        notes="Part of Mukesh Ambani's media conglomerate."
    ),
    "thewire.in": SourceMetadata(
        name="The Wire",
        ownership="Foundation for Independent Journalism (Non-profit)",
        funding="Grants & Individual Donations",
        ideological_lean="Left",
        notes="Aggressively critical of the establishment; focuses on civil liberties."
    ),
    "theprint.in": SourceMetadata(
        name="The Print",
        ownership="Shekhar Gupta (Printline Media)",
        funding="Corporate Investment & Ads",
        ideological_lean="Center",
        notes="Focuses on policy and strategic affairs; often features diverse op-eds."
    ),
    "thequint.com": SourceMetadata(
        name="The Quint",
        ownership="Raghav Bahl (Quint Digital Media)",
        funding="Advertising & Subscriptions",
        ideological_lean="Center-Left",
        notes="Digital-first outlet with a strong focus on social justice and political critique."
    ),
    "outlookindia.com": SourceMetadata(
        name="Outlook India",
        ownership="Rajan Raheja Group",
        funding="Advertising",
        ideological_lean="Center-Left",
        notes="Known for deep-dive features and investigative cover stories."
    ),
    "scroll.in": SourceMetadata(
        name="Scroll.in",
        ownership="Independent Media Writer's Association",
        funding="Omidyar Network & Individual Donations",
        ideological_lean="Left",
        notes="Strong focus on social issues and cultural reporting."
    ),
    "swarajyamag.com": SourceMetadata(
        name="Swarajya",
        ownership="Kovai Media Services",
        funding="Subscriptions & Ads",
        ideological_lean="Right",
        notes="Self-described as 'liberal center-right'; focuses on Indic civilization and economics."
    ),
    "opindia.com": SourceMetadata(
        name="OpIndia",
        ownership="Aasthi Media",
        funding="Advertising & Donations",
        ideological_lean="Right",
        notes="Digital-first outlet; often focuses on 'fact-checking' mainstream media from a right-wing lens."
    ),
    "newslaundry.com": SourceMetadata(
        name="Newslaundry",
        ownership="Independent (Madhu Trehan et al)",
        funding="Ad-free / Subscriber-funded",
        ideological_lean="Center-Left",
        notes="Media critique focus; strictly ad-free."
    ),
    "indiatimes.com": SourceMetadata(
        name="The Times of India / Navbharat Times",
        ownership="Bennett, Coleman and Co. Ltd (Jain Family)",
        funding="Advertising (High volume)",
        ideological_lean="Center-Right",
        notes="World's largest-circulated English daily; often pragmatic and pro-business."
    ),
    "jagran.com": SourceMetadata(
        name="Dainik Jagran",
        ownership="Jagran Prakashan Limited",
        funding="Advertising",
        ideological_lean="Right",
        notes="India's largest-read daily; known for a conservative, nationalist stance."
    ),
    "amarujala.com": SourceMetadata(
        name="Amar Ujala",
        ownership="Amar Ujala Publications",
        funding="Advertising",
        ideological_lean="Center-Right",
        notes="Strong presence in North India."
    ),
    "bhaskar.com": SourceMetadata(
        name="Dainik Bhaskar",
        ownership="DB Corp Ltd. (Agarwal Family)",
        funding="Advertising",
        ideological_lean="Center",
        notes="Largest newspaper group in India by circulation; often independent in its regional reporting."
    ),
    "sakal.com": SourceMetadata(
        name="Sakal",
        ownership="Sakal Media Group (Pawar Family)",
        funding="Advertising",
        ideological_lean="Center",
        notes="Major Marathi daily with deep regional influence."
    ),
    "lokmat.com": SourceMetadata(
        name="Lokmat",
        ownership="Darda Family",
        funding="Advertising",
        ideological_lean="Center",
        notes="Leading Marathi newspaper with vast rural reach."
    ),
    "anandabazar.com": SourceMetadata(
        name="Anandabazar Patrika",
        ownership="ABP Group (Sarkar Family)",
        funding="Advertising",
        ideological_lean="Center-Left",
        notes="Dominant Bengali daily; historical center of Bengali journalism."
    ),
    "mathrubhumi.com": SourceMetadata(
        name="Mathrubhumi",
        ownership="The Mathrubhumi Printing & Publishing Co. Ltd",
        funding="Advertising",
        ideological_lean="Center-Left",
        notes="Major Malayalam daily with a strong legacy of independence."
    ),
    "prajavani.net": SourceMetadata(
        name="Prajavani",
        ownership="The Printers (Mysore) Private Limited",
        funding="Advertising",
        ideological_lean="Center-Left",
        notes="Leading Kannada newspaper known for its progressive stance."
    ),
    "eenadu.net": SourceMetadata(
        name="Eenadu",
        ownership="Ramoji Group",
        funding="Advertising",
        ideological_lean="Center-Right",
        notes="Largest circulated Telugu newspaper; influential in regional politics."
    )
}

def get_source_metadata(url_or_domain: str) -> Optional[SourceMetadata]:
    """
    Robustly extracts the registered domain (e.g., indiatimes.com) 
    and looks it up in the Source Knowledge Base.
    """
    if not url_or_domain:
        return None
        
    extracted = tldextract.extract(url_or_domain)
    registered_domain = extracted.registered_domain.lower()
    
    return SOURCE_KB.get(registered_domain)
