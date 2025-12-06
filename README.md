# text2image-image2story

## 🌟 Overview

The **MLSE Project** is a versatile Streamlit web application that harnesses the power of the Google **Gemini API** for multi-modal and advanced natural language generation tasks. This suite offers two core creative functionalities: a **Visual Storyteller** that turns images into short fiction, and an **AI Image Generator** that uses Gemini for advanced prompt engineering before generating the final artwork.

***

## ✨ Features

The application is structured into two main tabs:

### 📖 1. Visual Storyteller (Image to Story)
* **Multi-modal Input:** Accepts an image (`.jpg`, `.png`, `.webp`).
* **Flash Fiction:** Uses the `gemini-2.5-flash` model to generate a **Flash Fiction** story, strictly based on the visual details in the image.
* **Constraints:** Stories are kept under **100 words** and include a bold title.

### 🖼️ 2. AI Image Generator (Text to Image)
* **Gemini Prompt Enhancement:** The core feature is using `gemini-2.5-flash` as an **"expert Prompt Engineer"** to transform a simple user idea (e.g., "A cat in space") into a detailed, high-quality prompt, including keywords for lighting, art style, camera angles, and texture.
* **Image Generation:** The enhanced prompt is then passed to the **Puter.js** SDK (specifically `puter.ai.txt2img`) for client-side image generation.

***

## 🛠️ Technologies Used

| Category | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend/Framework** | Python | Core programming language |
| **Web App** | Streamlit | Rapid application UI development |
| **AI/LLM** | `google-generativeai` | Interacting with the Gemini API (e.g., `gemini-2.5-flash`) |
| **Image Handling** | `Pillow` (PIL) | Opening and processing uploaded images |
| **Image Generation** | Puter.js SDK | Client-side Text-to-Image generation |

***

## 🚀 Installation and Setup

### Prerequisites
1.  **Python 3.x**
2.  A **Gemini API Key**. Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Step-by-Step Guide
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/ujjwal1011/text2image-image2story.git](https://github.com/ujjwal1011/text2image-image2story.git)
    cd text2image-image2story
    ```

2.  **Install Dependencies:**
    Create a virtual environment (recommended) and install the necessary packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**
    Start the Streamlit application from the terminal.
    ```bash
    streamlit run app.py
    ```
    The application will automatically open in your web browser (usually at `http://localhost:8501`).

***

## ⚙️ Usage

1.  **Enter API Key:** Paste your **Gemini API Key** into the text input field in the sidebar.
2.  **Select a Mode:**
    * Go to the **"📖 Image to Story"** tab, upload an image, and click **"Generate Story"**.
    * Go to the **"🖼️ Text to Image Generator"** tab, enter a simple idea (the raw prompt), and click **"✨ Enhance & Generate Image"**.

***

## 👨‍💻 Code Explanation (`app.py`)

### 1. Configuration & Setup
The script begins by importing necessary libraries (`streamlit`, `google.generativeai`, `PIL.Image`, `html`, `textwrap`). The API key is securely collected using `st.text_input(type="password")` in the sidebar.

### 2. `generate_story(api_key, image, prompt, temperature=0.7)`
* **Purpose:** Handles the Image-to-Story functionality.
* **Logic:** It uses a highly specific **Meta-Prompt** to instruct `gemini-2.5-flash` to act as a **"master of 'Flash Fiction'"**. The prompt mandates specific details like describing objects/colors, adhering to a 100-word limit, and including a bold title.

### 3. `enhance_image_prompt(api_key, raw_prompt)`
* **Purpose:** Handles the Text-to-Image prompt enhancement.
* **Logic:** It employs a different **Meta-Prompt** instructing `gemini-2.5-flash` to act as an **"expert Prompt Engineer"**. The goal is to rewrite the raw idea into a highly descriptive prompt suitable for modern AI image models (e.g., Stable Diffusion), focusing on technical details like style and lighting.

### 4. Image Generation via Streamlit Components
* The application uses the enhanced prompt to dynamically construct an **HTML** payload using the `textwrap.dedent` and `html.escape` functions.
* This HTML includes a JavaScript script that loads the **Puter.js SDK** and calls the client-side **`puter.ai.txt2img(promptText)`** function, ensuring the image generation happens securely outside of the Streamlit server. The result is rendered inside the Streamlit app using `st.components.v1.html()`.

***

## 📈 Future Enhancements

The following features are planned for future versions to improve usability and functionality:

* **Model Selection:** Introduce an option for users to select different Gemini models (e.g., `gemini-2.5-pro` for higher-quality stories or more complex prompt engineering).
* **Hyperparameter Control:** Add sliders for **`temperature`** control in both modes to allow users to adjust the creativity/randomness of the AI's output.
* **Native Image Generation (If Available):** Explore replacing the current client-side Puter.js solution with a server-side, native image generation API call if a robust and integrated solution becomes available via the Gemini ecosystem.
* **Result Gallery:** Implement a mechanism to store and display the history of generated images and stories within the session.
* **Image-to-Image / Prompt Editing:** Add advanced image generation options, such as allowing users to upload a base image to modify (Image-to-Image) or further edit the enhanced prompt before generation.

***

## 📂 Project Structure (Simplified)
