from flask import Flask, request, jsonify
from flask_cors import CORS
from agent_core import run_analysis, analyze_draft
from campaign_agent import generate_campaign_schedule
from tools.linkedin_tool import post_to_linkedin
from tools.image_gen import generate_image
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

load_dotenv() # Load env vars from .env

app = Flask(__name__)
# Configure Upload Folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)  # Enable CORS for all routes

@app.route('/analyze_draft', methods=['POST'])
def analyze_draft_route():
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image file provided"}), 400
        
    file = request.files['image']
    caption = request.form.get('caption', '')
    
    if file.filename == '':
        return jsonify({"success": False, "error": "No selected file"}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Analyze
        result = analyze_draft(filepath, caption)
        
        # Optional: Clean up file after analysis? For now keep it.
        return jsonify(result)

@app.route('/generate_campaign', methods=['POST'])
def generate_campaign():
    data = request.json
    strategy = data.get('strategy')
    days = data.get('days', 5)
    visual_description = data.get('visual_description', "")
    
    if not strategy:
        return jsonify({"success": False, "error": "No strategy provided"}), 400
        
    result = generate_campaign_schedule(strategy, days, visual_description)
    return jsonify(result)

@app.route('/post_update', methods=['POST'])
def post_update():
    data = request.json
    text = data.get('text')
    
    # Use global state for token/urn
    # In production, receive this from frontend (localStorage)
    access_token = APP_STATE["linkedin_access_token"]
    urn = APP_STATE["linkedin_urn"]
    
    if not access_token:
         return jsonify({"success": False, "error": "Not connected to LinkedIn"}), 401
         
    result = post_to_linkedin(text, access_token, urn)
    return jsonify(result)



@app.route('/generate_image_for_post', methods=['POST'])
def generate_image_route():
    data = request.json
    prompt = data.get('prompt')
    
    if not prompt:
        return jsonify({"success": False, "error": "No prompt provided"}), 400
        
    try:
        # Generate PIL Image
        img = generate_image(prompt)
        
        if img:
            # Save to uploads
            import uuid
            filename = f"generated_{uuid.uuid4().hex}.png"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            img.save(filepath)
            
            # Return URL (assuming static file serving needs setup or just direct use)
            # For this simple flask setup, we need a route to serve uploads or just return local path for now?
            # Actually, standard flask doesn't serve 'uploads' by default unless configured.
            # We will add a route to serve these files or use a data URI if small. 
            # Let's return a relative URL and add a static route.
            return jsonify({
                "success": True, 
                "image_url": f"http://127.0.0.1:5000/uploads/{filename}"
            })
        else:
            return jsonify({"success": False, "error": "Image generation failed"}), 500

    except Exception as e:
        print(f"Gen Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "running", "message": "Backend Agent Server is up and running. Use POST /analyze to analyze data."})

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    # Handle both GET (browser/query param) and POST (API/JSON)
    if request.method == 'GET':
        url = request.args.get('url')
    else:
        data = request.json or {}
        url = data.get('url')
    
    # Default to "demo" (local file) if no URL provided
    if not url:
        url = "demo"
    
    print(f"Received request to analyze: {url} (Method: {request.method})")
    
    # Detect platform
    platform = "linkedin"
    if url and "instagram" in url.lower():
        platform = "instagram"
    
    # In a real production app, we would scrape the URL (LinkedIn/Instagram) here.
    # For this Hackathon implementation, we use the local 'linkedin_comments.json'
    # as our data source to demonstrate the Multi-Agent capabilities.
    
    try:
        # Run the agent logic
        # We assume linkedin_comments.json is in the same directory
        # In the future, 'url' could determine which file or scraper to use.
        results = run_analysis("linkedin_comments.json", platform=platform)
        
        if results.get("error"):
            return jsonify({"success": False, "error": results["error"]}), 500
            
        return jsonify({
            "success": True,
            "data": {
                "summary": "Analysis of LinkedIn comments for the campaign.",
                "youth_insight": results["youth_analysis"],
                "adult_insight": results["adult_analysis"],
                "strategy": results["strategy"]
            }
        })
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

from auth_utils import get_linkedin_auth_url, exchange_code_for_token, get_user_info

# --- Global Storage (For Demo Purposes) ---
# In production, use a database or session
APP_STATE = {
    "linkedin_access_token": None,
    "linkedin_urn": None
}

@app.route('/auth/linkedin', methods=['GET'])
def auth_linkedin():
    try:
        url = get_linkedin_auth_url()
        return jsonify({"url": url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/auth/callback', methods=['GET'])
def auth_callback():
    code = request.args.get('code')
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        # 1. Exchange code for token
        token_data = exchange_code_for_token(code)
        access_token = token_data.get('access_token')
        
        # 2. Get User URN
        user_info = get_user_info(access_token)
        urn = f"urn:li:person:{user_info.get('sub')}"
        
        # 3. Store in Memory
        APP_STATE["linkedin_access_token"] = access_token
        APP_STATE["linkedin_urn"] = urn
        
        # 4. Redirect back to frontend (Dashboard)
        # Assuming frontend is on standard port, or just close window
        # For this demo, we can redirect to the dashboard.
        return f"<script>window.location.href = 'http://localhost:8000/dashboard.html';</script> Redirecting..."
        
    except Exception as e:
        print(f"Auth Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({
        "linkedin_connected": APP_STATE["linkedin_access_token"] is not None,
        "linkedin_urn": APP_STATE["linkedin_urn"]
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
