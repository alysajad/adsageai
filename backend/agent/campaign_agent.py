from google import genai
from google.genai import types
import os
import json

import ast

def generate_campaign_schedule(strategy_context, days=5, visual_description=""):
    """
    Generates a social media campaign schedule based on the strategy.
    """
    try:
        client = genai.Client()
        
        # Load Prompt
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(base_dir, "prompts", "campaign_creator.prompt")
        
        with open(prompt_path, "r") as f:
            instructions = f.read()
            
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=instructions
            )
        )
        
        message = f"""
        STRATEGY CONTEXT:
        {strategy_context}
        
        VISUAL CONTEXT (REFERENCE IMAGE DESCRIPTION):
        {visual_description}
        
        INSRUCTION:
        You must generate a UNIQUE 'image_prompt' for each day that visualizes that specific day's topic.
        
        CRITICAL RULES FOR IMAGE PROMPTS:
        1. **Keep the Subject/Style**: You MUST strictly use the visual details from the VISUAL CONTEXT (characters, setting, colors, lighting) as the *base*.
        2. **Vary the Action/Shot**: Do NOT just repeat the visual context. You MUST change the camera angle, the character's action, or the specific focus to match the day's `topic`.
        3. **Example**: If the context is "A cybernetic banana in a neon room":
           - Day 1 (Launch): "Close-up of the cybernetic banana pressing a holographic launch button in the neon room."
           - Day 2 (Relax): "Wide shot of the cybernetic banana lounging on a floaty chair in the same neon room."
        
        CAMPAIGN DURATION:
        {days} Days
        """
        
        response = chat.send_message(message=message)
        
        # Clean up response (in case of markdown blocks)
        raw_text = response.text.replace("```json", "").replace("```", "").strip()
        
        try:
            campaign_data = json.loads(raw_text)
        except Exception as e_json:
            print(f"Campaign JSON Error: {e_json}. Attempting fallback...")
            try:
                campaign_data = ast.literal_eval(raw_text)
            except Exception as e2:
                print(f"Campaign Critical Parse Error: {e2}")
                return {"success": False, "error": f"Failed to parse campaign: {e2}"}

        return {"success": True, "campaign": campaign_data}
        
    except Exception as e:
        print(f"Campaign Agent Error: {e}")
        return {"success": False, "error": str(e)}
