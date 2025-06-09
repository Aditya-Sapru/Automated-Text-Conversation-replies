import streamlit as st
import requests
import base64
import os
from PIL import Image
import io
import json
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("DEBUG: All imports successful")

# Configure Streamlit page
st.set_page_config(
    page_title="AI Commenter",
    page_icon="💬",
    layout="wide"
)

print("DEBUG: Page config set")


class GeminiCommenter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    
    def encode_image_to_base64(self, image_file) -> str:
        """
        Convert uploaded image to base64 string.
        
        Base64 encoding process:
        1. Read image file as bytes
        2. Encode bytes to base64 string
        3. Decode to UTF-8 string for JSON compatibility
        """
        try:
            # Read image bytes
            image_bytes = image_file.read()
            
            # Encode to base64
            base64_string = base64.b64encode(image_bytes).decode('utf-8')
            
            return base64_string
        except Exception as e:
            st.error(f"Error encoding image: {str(e)}")
            return None
    
    def create_prompt(self, tone: str) -> str:
        """Create system prompt based on desired tone"""
        base_prompt = """
        You are an AI assistant that analyzes text conversations from images and generates appropriate replies.
        
        Instructions:
        1. Carefully read and understand the conversation context from the image
        2. Identify the last message that needs a response
        3. Generate a contextually appropriate reply in the specified tone
        4. Keep the response natural and conversational
        5. Match the communication style of the conversation
        
        """
        
        tone_instructions = {
            "excited": "Respond with high energy, enthusiasm, and exclamation marks!",
            "happy": "Respond with positivity, warmth, and cheerfulness.",
            "sad": "Respond with empathy, understanding, and gentle support.",
            "romantic": "Respond with affection, sweetness, and romantic undertones.",
            "casual": "Respond in a relaxed, informal, and friendly manner.",
            "professional": "Respond formally and professionally.",
            "funny": "Respond with humor, wit, and playfulness.",
            "supportive": "Respond with encouragement and emotional support.",
            "sarcastic": "Respond with subtle sarcasm and wit.",
            "caring": "Respond with genuine care and concern."
        }
        
        tone_instruction = tone_instructions.get(tone.lower(), f"Respond in a {tone} tone.")
        
        return base_prompt + f"\nTone: {tone_instruction}\n\nPlease provide only the reply message, nothing else."
    
    def generate_comment(self, image_base64: str, tone: str) -> Optional[str]:
        """Send request to Gemini API and get response"""
        try:
            # Create request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": self.create_prompt(tone)
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ]
            }
            
            # Make API request
            url = f"{self.base_url}?key={self.api_key}"
            headers = {
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract generated text from response
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    return content.strip()
                else:
                    st.error("No response generated from API")
                    return None
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            st.error(f"Error calling Gemini API: {str(e)}")
            return None

def main():
    st.title("🤖 AI Commenter Bot")
    st.markdown("Upload a conversation screenshot and get the perfect reply!")
    
    # Load API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("⚠️ GEMINI_API_KEY not found in environment variables!")
        st.info("Please set your Gemini API key in the .env file")
        st.stop()
    
    # Initialize commenter
    commenter = GeminiCommenter(api_key)
    
    # Create two columns
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📤 Input")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "Upload conversation screenshot",
            type=['png', 'jpg', 'jpeg'],
            help="Upload an image containing a text conversation"
        )
        
        # Tone selection
        tone_options = [
            "excited", "happy", "sad", "romantic", "casual", 
            "professional", "funny", "supportive", "sarcastic", "caring"
        ]
        
        selected_tone = st.selectbox(
            "Select response tone:",
            options=tone_options,
            index=0,
            help="Choose the tone for your AI response"
        )
        
        # Custom tone input
        custom_tone = st.text_input(
            "Or enter custom tone:",
            placeholder="e.g., enthusiastic, witty, empathetic..."
        )
        
        # Use custom tone if provided
        final_tone = custom_tone if custom_tone.strip() else selected_tone
        
        # Generate button
        generate_btn = st.button("🚀 Generate Reply", type="primary")
        
        # Display uploaded image
        if uploaded_file:
            st.subheader("📷 Uploaded Image")
            image = Image.open(uploaded_file)
            st.image(image, caption="Conversation Screenshot", use_container_width=True)
    
    with col2:
        st.header("📥 Output")
        
        if generate_btn and uploaded_file:
            # Show processing message
            with st.spinner("🧠 AI is analyzing the conversation..."):
                
                # Reset file pointer
                uploaded_file.seek(0)
                
                # Encode image to base64
                base64_image = commenter.encode_image_to_base64(uploaded_file)
                
                if base64_image:
                    # Generate comment
                    reply = commenter.generate_comment(base64_image, final_tone)
                    
                    if reply:
                        st.success("✅ Reply generated successfully!")
                        
                        # Display the reply
                        st.subheader("💬 AI Generated Reply")
                        st.markdown(f"**Tone:** {final_tone}")
                        
                        # Style the reply box
                        st.markdown(
                            f"""
                            <div style="
                                background-color: #f0f2f6;
                                padding: 20px;
                                border-radius: 10px;
                                border-left: 4px solid #4CAF50;
                                margin: 10px 0;
                            ">
                                <p style="margin: 0; font-size: 16px; line-height: 1.5;">
                                    {reply}
                                </p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Copy to clipboard button
                        st.code(reply, language=None)
                        st.info("💡 Use the copy button above to copy the reply!")
                    
        elif generate_btn and not uploaded_file:
            st.warning("⚠️ Please upload an image first!")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.markdown("""
        This AI Commenter Bot uses Google's Gemini 1.5 Flash model to:
        
        1. **Analyze** conversation screenshots
        2. **Understand** context and flow
        3. **Generate** appropriate replies in your desired tone
        
        ### 🔧 How it works:
        - Upload an image of a text conversation
        - Select or enter a tone
        - AI reads the conversation and generates a reply
        
        ### 📝 Base64 Encoding:
        Images are converted to base64 strings for API transmission:
        1. Image → Binary data
        2. Binary → Base64 string
        3. Send to Gemini API
        """)
        
        st.header("💡 Tips")
        st.markdown("""
        - Use clear, readable screenshots
        - Try different tones for variety
        - Works with any messaging app
        - Supports custom tone descriptions
        """)
        
        st.header("🎯 Supported Tones")
        for tone in tone_options:
            st.markdown(f"• {tone.title()}")

if __name__ == "__main__":
    main()