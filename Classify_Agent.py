import pandas as pd
import openai
from openai import OpenAI

# ------------ CONFIG ------------
API_KEY = "your_key_here"
INPUT_FILE = "apartments_unclassified.xlsx"
OUTPUT_FILE = "apartments_with_neighborhoods.xlsx"
ADDRESS_COLUMN = "address"


NEIGHBORHOODS = [
    "Adams", "Admiral", "Alki", "Alki Point", "Arbor Heights", "Atlantic",
    "Atlantic City Beach", "Ballard", "Beacon Hill", "Belltown", "Bitter Lake",
    "Blue Ridge", "Briarcliff", "Brighton", "Broadmoor", "Broadview", "Broadway",
    "Bryant", "Capitol Hill", "Cascade", "Cedar Park", "Central Business District",
    "Central District", "Central Waterfront", "Cherry Hill",
    "Chinatown-International District", "Columbia City", "Crown Hill", "Delridge",
    "Denny-Blaine", "Denny Triangle", "Downtown", "Dunlap", "East Queen Anne",
    "Eastlake", "Fairmount Park", "Fauntleroy", "First Hill", "Fremont", "Gatewood",
    "Genesee", "Georgetown", "Green Lake", "Greenwood", "Haller Lake", "Harbor Island",
    "Hawthorne Hills", "Highland Park", "Hillman City", "Holly Park",
    "Industrial District", "Interbay", "International District", "Judkins Park",
    "Junction", "Lake City", "Lakewood", "Laurelhurst", "Lawton Park", "Leschi",
    "Licton Springs", "Lincoln Park", "Little Saigon", "Loyal Heights",
    "Lower Queen Anne", "Madison Park", "Madison Valley", "Madrona", "Madrona Valley",
    "Magnolia", "Mann", "Maple Leaf", "Matthews Beach", "Meadowbrook",
    "Mid Beacon Hill", "Minor", "Montlake", "Morgan Junction", "Mount Baker",
    "North Beach", "North Beacon Hill", "North Delridge", "North Queen Anne",
    "Northgate", "Olympic Hills", "Phinney Ridge", "Pike-Market", "Pinehurst",
    "Pioneer Square", "Portage Bay", "Queen Anne", "Rainier Beach", "Rainier Valley",
    "Rainier View", "Ravenna", "Riverview", "Roosevelt", "Roxhill", "Sand Point",
    "Seaview", "Seward Park", "South Delridge", "South Lake Union", "South Park",
    "South Beacon Hill", "Stevens", "Sunset Hill", "University District",
    "Victory Heights", "View Ridge", "Wallingford", "Washington Park", "Wedgwood",
    "West Edge", "West Queen Anne", "West Seattle", "West Woodland", "Westlake",
    "Whittier Heights", "Windermere", "Yesler Terrace"
]


PROMPT_TEMPLATE = """
please classify this {address} to one of the following neighbor in the {choices}, 
 
to improve accuracy, pay extra attention to the 5 digits post code. That's where you can get the accurate information

remember only return the name of the neighbor. 
"""

openai.api_key = API_KEY
client = OpenAI(
    api_key=openai.api_key,
)

def classify_address_with_gpt(address):
    prompt = PROMPT_TEMPLATE.format(
        address=address,
        choices="\n".join(f"- {n}" for n in NEIGHBORHOODS)
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def classify_excel_addresses():
    xls = pd.ExcelFile(INPUT_FILE)
    writer = pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl")

    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        if ADDRESS_COLUMN not in df.columns:
            df["GPT classification"] = "N/A"
        else:
            df["GPT classification"] = df[ADDRESS_COLUMN].apply(classify_address_with_gpt)
            df = df.sort_values(by="GPT classification")  
        df.to_excel(writer, sheet_name=sheet_name[:31], index=False)

    writer.close()
    print(f"classified file: {OUTPUT_FILE}")


classify_excel_addresses()

