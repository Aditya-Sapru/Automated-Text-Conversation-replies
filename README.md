# 🤖 AI Commenter Bot using Streamlit + Gemini API

This is a Streamlit web app that allows users to upload an image — either a **conversation screenshot** or a **regular social media post** — and generates a **contextually relevant reply** or **comment** based on a tone selected by the user.

---

## 🚀 Features

- 📷 Upload images (conversations or photos)
- 🧠 Uses **Google's Gemini 1.5 Flash model** for content understanding
- 💬 Generates natural and smart replies or comments
- 🎭 Customizable tone: Excited, Romantic, Professional, Funny, Supportive, etc.
- 🌈 Supports both **predefined** and **custom** tone inputs
- 📄 Stylish and easy-to-use Streamlit interface

---

## 🧠 How It Works

1. User uploads an image of a conversation or a post.
2. The image is converted into a base64 format.
3. A prompt is constructed based on the selected tone.
4. The image and prompt are sent to Gemini API.
5. The API responds with an appropriate reply or comment.
6. The app displays the generated text to the user.

