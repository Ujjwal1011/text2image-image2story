import streamlit as st
import google.generativeai as genai
from PIL import Image
import html
from textwrap import dedent

# --- Page Configuration ---
st.set_page_config(
    page_title="Gemini Creative Suite",
    page_icon="🎨",
    layout="centered"
)

# --- Sidebar: API Key Configuration ---
with st.sidebar:
    st.header("🔑 Configuration")
    api_key = st.text_input("Enter your Gemini API Key", type="password")
    st.markdown("[Get your API Key here](https://aistudio.google.com/app/apikey)")
    
    st.divider()
    st.caption("App Modes:")
    st.caption("1. **Image to Story:** Upload image -> Gemini Story")
    st.caption("2. **Text to Image:** Prompt -> Gemini Enhancer -> Puter Generator")

# --- Function: Image to Story (Tab 1) ---
def generate_story(api_key, image, prompt, temperature=0.7):
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash', generation_config={"temperature": temperature})
        
        full_prompt = (
            "Act as a master of 'Flash Fiction'. Write a story strictly based on the visual details in the image.\n"
            f"**USER THEME:** '{prompt}'\n"
            "**INSTRUCTIONS:**\n"
            "1. Describe specific objects/colors visible in the image.\n"
            "2. Keep it under 100 words.\n"
            "3. Include a Title in bold."
        )
        response = model.generate_content([full_prompt, image])
        return response.text
    except Exception as e:
        return f"Error: {e}"

# --- Function: Enhance Prompt (Tab 2) ---
def enhance_image_prompt(api_key, raw_prompt):
    """Uses Gemini to turn a simple idea into a detailed image generation prompt."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        meta_prompt = (
            "You are an expert Prompt Engineer for AI Image Generators (like Stable Diffusion). "
            f"Take this raw user idea: '{raw_prompt}'.\n"
            "Rewrite it into a detailed, high-quality image prompt. "
            "Include keywords about lighting, art style (photorealistic, cinematic, oil painting, etc.), "
            "camera angles, and texture. "
            "Output ONLY the final prompt text. Do not add explanations."
        )
        
        response = model.generate_content(meta_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# --- Main Layout ---
st.title("🎨 Gemini Creative Suite")

# Create Tabs
tab1, tab2 = st.tabs(["📖 Image to Story", "🖼️ Text to Image Generator"])

# ==========================================
# TAB 1: VISUAL STORYTELLER (Existing Logic)
# ==========================================
with tab1:
    st.header("Visual Storyteller")
    st.write("Upload an image, and Gemini will write a 100-word story about it.")
    
    img_file = st.file_uploader("Upload Image", type=["jpg", "png", "webp"])
    story_prompt = st.text_area("Theme/Context (Optional)", placeholder="e.g., A sad memory...")
    
    if st.button("Generate Story"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar.")
        elif not img_file:
            st.warning("Please upload an image.")
        else:
            with st.spinner("Gemini is writing..."):
                image = Image.open(img_file)
                st.image(image, width=300)
                story = generate_story(api_key, image, story_prompt)
                st.markdown(story)

# ==========================================
# TAB 2: IMAGE GENERATOR (Puter + Gemini)
# ==========================================
with tab2:
    st.header("AI Image Generator")
    st.write("Enter a simple idea. Gemini will enhance it, and Puter.js will generate it.")

    raw_prompt = st.text_area("Enter your idea", placeholder="A cat in space", height=100)
    
    if st.button("✨ Enhance & Generate Image"):
        if not api_key:
            st.error("Please enter your API Key in the sidebar (needed for the enhancement step).")
        elif not raw_prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            # 1. Enhance Prompt using Gemini
            with st.spinner("Gemini is enhancing your prompt for better results..."):
                enhanced_prompt = enhance_image_prompt(api_key, raw_prompt)
            
            # Check if Gemini failed
            if "Error:" in enhanced_prompt:
                st.error(enhanced_prompt)
            else:
                st.success("Prompt Enhanced!")
                with st.expander("View Enhanced Prompt"):
                    st.write(enhanced_prompt)

                # 2. Generate Image using Puter JS
                # We inject the 'enhanced_prompt' into the HTML string
                safe_prompt = html.escape(enhanced_prompt)

                html_code = dedent(f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="utf-8"/>
                    <script src="https://js.puter.com/v2/" 
                            onerror="document.getElementById('status').innerHTML='❌ <b>Error:</b> Failed to load Puter SDK.<br>Please disable AdBlockers or check your internet connection.'; document.getElementById('status').style.color='red';">
                    </script>
                    <style>
                        body {{ font-family: sans-serif; padding: 10px; text-align: center; }}
                        #status {{ margin: 12px 0; font-weight: bold; color: #333; }}
                        img {{ max-width: 100%; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                        .container {{ display: flex; flex-direction: column; align-items: center; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h3>🎨 Generating your masterpiece...</h3>
                        <div id="status">Initializing Puter SDK...</div>
                        <div id="output"></div>
                    </div>

                    <script>
                    async function generateImage() {{
                        try {{
                            // Check if 'puter' loaded correctly
                            if (typeof puter === 'undefined') {{
                                throw new Error("Puter SDK is not defined. The script failed to load.");
                            }}

                            let status = document.getElementById("status");
                            status.textContent = "Requesting GPU (puter.ai.txt2img)...";

                            const promptText = "{safe_prompt}";
                            
                            // Call Puter API
                            const img = await puter.ai.txt2img(promptText);

                            const out = document.getElementById("output");
                            status.textContent = "Processing response...";

                            if (img instanceof HTMLImageElement) {{
                                out.appendChild(img);
                                status.textContent = "✨ Generation Complete!";
                            }} 
                            else if (typeof img === "string") {{
                                let i = document.createElement("img");
                                i.src = img;
                                out.appendChild(i);
                                status.textContent = "✨ Generation Complete!";
                            }} 
                            else {{
                                status.textContent = "Unexpected format returned.";
                                console.log(img);
                            }}
                        }} catch (err) {{
                            document.getElementById("status").innerHTML = "❌ <b>Error:</b> " + err.message;
                            document.getElementById("status").style.color = "red";
                            console.error(err);
                        }}
                    }}

                    // Wait 1 second before starting to ensure script is ready
                    setTimeout(generateImage, 1000);
                    </script>
                </body>
                </html>
                """)
                # Render the HTML component
                st.components.v1.html(html_code, height=600, scrolling=True)