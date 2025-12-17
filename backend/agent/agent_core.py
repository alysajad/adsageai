from google import genai
from google.genai import types
from tools.load_json import load_linkedin_comments
try:
    from backend.agent.hashtag_scraper import scrape_hashtags
except ImportError:
    try:
        from agent.hashtag_scraper import scrape_hashtags
    except ImportError:
         from hashtag_scraper import scrape_hashtags
from PIL import Image
import os
import json
import ast

def run_analysis(data_file="linkedin_comments.json", platform="linkedin"):
    """
    Runs the multi-agent analysis.
    platform: 'linkedin' or 'instagram'
    """
    results = {
        "youth_analysis": "",
        "adult_analysis": "",
        "strategy": "",
        "error": None
    }

    print(f"STEP 1: Starting analysis on {data_file} for {platform}...")

    try:
        client = genai.Client()
        print("STEP 2: Client created successfully.")
    except Exception as e:
        error_msg = f"Failed to create genai client: {e}"
        print(f"❌ ERROR: {error_msg}")
        results["error"] = error_msg
        return results

    # Helper to load prompts safely
    def load_prompt(filename):
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "prompts", filename)
            with open(path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"❌ ERROR: Cannot load prompt {filename}: {e}")
            return None

    # Determine Prompts based on Platform
    if platform.lower() == "instagram":
        prompt_youth = "analyze_instagram_18_30.prompt"
        prompt_adult = "analyze_instagram_30_50.prompt"
        data_source_name = "instagram_comments.json" # Assuming we might want to differentiate later, or re-use logic
    else:
        prompt_youth = "analyze_campaign.prompt"
        prompt_adult = "analyze_campaign_30_50.prompt"
        data_source_name = "linkedin_comments.json"
        
    # Fallback to existing file if specific one missing (for hackathon demo)
    if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", data_source_name)):
         # If instagram file doesn't exist, use the linkedin one as mock data or whatever was passed
         data_source_name = data_file 

    # --- Agent for 18-30 Age Group ---
    try:
        instructions = load_prompt(prompt_youth)
        if not instructions:
            raise Exception(f"Failed to load {prompt_youth}")
        
        print(f"STEP 3: Loaded prompt (18-30) for {platform}.")

        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[load_linkedin_comments],
                system_instruction=instructions
            )
        )
        print("STEP 4: Chat session (18-30) created.")

        print("STEP 5: Sending message to agent (18-30)...")
        
        response = chat.send_message(
            message=f"Please load the comments from '{data_source_name}' and analyze them according to the instructions for {platform}."
        )

        print("STEP 6: Response (18-30) received.")
        results["youth_analysis"] = response.text

    except Exception as e:
        print(f"❌ ERROR during 18-30 agent execution: {e}")

    # --- Agent for 30-50 Age Group ---
    print("-" * 30)
    try:
        instructions_30_50 = load_prompt(prompt_adult)
        if not instructions_30_50:
            raise Exception(f"Failed to load {prompt_adult}")
            
        print(f"STEP 7: Loaded 30-50 prompt for {platform}.")
        
        chat_30_50 = client.chats.create(
            model="gemini-2.5-flash", 
            config=types.GenerateContentConfig(
                tools=[load_linkedin_comments],
                system_instruction=instructions_30_50
            )
        )
        print("STEP 8: Chat session (30-50) created.")
        
        print("STEP 9: Sending message to agent (30-50)...")
        response_30_50 = chat_30_50.send_message(
            message=f"Please load the comments from '{data_source_name}' and analyze them for the 30-50 age group on {platform}."
        )
        
        print("STEP 10: Response (30-50) received.")
        results["adult_analysis"] = response_30_50.text
        
    except Exception as e:
        print(f"❌ ERROR during 30-50 agent execution: {e}")

    # --- Strategist Agent ---
    if results["youth_analysis"] and results["adult_analysis"]:
        print("-" * 30)
        try:
            instructions_strategist = load_prompt("negotiate_suggestions.prompt")
            if not instructions_strategist:
                raise Exception("Failed to load negotiate_suggestions.prompt")

            print("STEP 11: Loaded Strategist prompt.")
            
            chat_strategist = client.chats.create(
                model="gemini-2.5-flash", 
                config=types.GenerateContentConfig(
                    system_instruction=instructions_strategist
                )
            )
            print("STEP 12: Chat session (Strategist) created.")
            
            strategist_message = f"""
            Here is the analysis from the 18-30 Age Group:
            {results['youth_analysis']}
            
            Here is the analysis from the 30-50 Age Group:
            {results['adult_analysis']}
            
            Please negotiate and provide strategic suggestions based on these reports.
            """
            
            print("STEP 13: Sending message to Strategist Agent...")
            response_strategist = chat_strategist.send_message(message=strategist_message)
            
            print("STEP 14: STRATEGIST RESPONSE received.")
            results["strategy"] = response_strategist.text
            
        except Exception as e:
            print(f"❌ ERROR during Strategist execution: {e}")
            results["error"] = str(e) # Capture strategist error if it happens
    else:
        msg = "Skipping Strategist: Missing analysis from one or more groups."
        print(msg)
        if not results["error"]:
             results["error"] = msg

    return results

def analyze_draft(image_path, caption):
    """
    Analyzes a draft post (Image + Caption) using Gemini Vision.
    """
    results = {
        "success": False,
        "prediction": {},
        "error": None
    }
    
    print(f"STEP 1: Analyzing Draft - Image: {image_path}, Caption: {caption}")
    
    try:
        client = genai.Client()
        
        # Load Prompt
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_dir, "prompts", "predictive_analysis.prompt")
        
        with open(prompt_path, "r") as f:
            instructions = f.read()
            
        # Load Image
        image = Image.open(image_path)
        
        print("STEP 2: Sending to Gemini Vision...")
        
        # Create Chat with System Instructions
        # Note: For Vision, we often just generate_content with system_instruction in config
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image, f"Caption: {caption}"],
            config=types.GenerateContentConfig(
                system_instruction=instructions
            )
        )
        
        print("STEP 3: Response received.")
        
        # Clean and Parse JSON
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        
        try:
            data = json.loads(raw_text)
        except Exception as e_json:
            print(f"⚠️ JSON Parse Error ({e_json}). Attempting ast.literal_eval fallback...")
            try:
                # Fallback for single quotes or python-style dicts
                data = ast.literal_eval(raw_text)
            except Exception as e2:
                print(f"❌ Critical Parsing Error: {e2}")
                # Return a safe error structure so frontend doesn't crash
                data = {
                    "summary": "AI Error: Could not parse response.",
                    "predicted_engagement": 0,
                    "age_group_reactions": {"youth": "Error", "adult": "Error", "senior": "Error"},
                    "optimization_tips": ["Please retry analysis."],
                    "hashtags": []
                }
        
        results["success"] = True

        # Dynamic Hashtag Scraping Logic
        if "hashtag_search_query" in data and data["hashtag_search_query"]:
             query = data["hashtag_search_query"]
             print(f"STEP 4: Scraping hashtags for query: '{query}'...")
             scraped_tags = scrape_hashtags(query)
             if scraped_tags:
                 print(f"STEP 5: Found {len(scraped_tags)} dynamic hashtags.")
                 # Prioritize scraped tags, maybe keep a few AI ones if needed, or just replace.
                 # Strategy: Use scraped tags primarily.
                 data["hashtags"] = scraped_tags
             else:
                 print("STEP 5: No dynamic hashtags found, keeping AI suggestions.")
        
        results["prediction"] = data
        
    except Exception as e:
        print(f"❌ Analysis Error: {e}")
        results["error"] = str(e)
        
    return results
