#  Farm Advisor – AI-Based Crop & Field Analysis System

![Farm Advisor UI](./farm-advisor-ui.jpeg)

Farm Advisor is an **AI-powered smart farming application** that allows farmers to upload crop or field images and receive **instant AI-driven insights, analysis, and advisory recommendations**.

The system uses a **Hugging Face pre-trained model** for image analysis, with a **FastAPI backend** and a modern **React frontend**.

---

## About the Project

Traditional farming decisions often rely on experience and guesswork, which may lead to crop loss and reduced productivity.  
**Farm Advisor** leverages **Artificial Intelligence and Computer Vision** to help farmers make **data-driven decisions** using simple image uploads.

---

## Objectives

- Analyze crop or field images using AI
- Provide smart insights and recommendations
- Assist farmers with early detection of issues
- Improve agricultural productivity using technology

---

## Features

*  Upload crop or field images
*  AI-powered image analysis
*  Crop health & advisory insights
*  Fast response using Hugging Face Inference API
*  Clean and farmer-friendly UI
*  Dockerized frontend & backend

---

## How It Works

1. User uploads a crop/field image from the UI  
2. React frontend sends the image to FastAPI backend  
3. Backend calls **Hugging Face Inference API**  
4. AI model analyzes the image  
5. Prediction & insights are returned  
6. Results are displayed on the dashboard  

---

##  Tech Stack

### Frontend
* React.js
* HTML5, CSS3
* Deployed using GitHub Pages

### Backend
* FastAPI (Python)
* Hugging Face Inference API
* RESTful APIs

### DevOps
 * Docker
 * Docker Compose

---

##  Hugging Face Model Integration

The backend uses a **Hugging Face hosted pre-trained model** for image analysis.

### API Flow


### Sample Backend Code
     python
           
    import requests
    API_URL = "https://api-inference.huggingface.co/models/<your-model-name>"
    #headers = {
    "Authorization": "Bearer YOUR_HUGGINGFACE_API_TOKEN"
    }

    def analyze_image(image_bytes):
      response = requests.post(API_URL, headers=headers, data=image_bytes)
      return response.json()

---

## 📂 Project Structure

    Farm-Advisor/
    │
    ├── backend/
    │   ├── main.py
    │   ├── requirements.txt
    │   └── Dockerfile.backend
    │
    ├── frontend/
    │   ├── src/
    │   ├── public/
    │   └── Dockerfile.frontend
    │
    ├── docs/                 
    ├── docker-compose.yml
    ├── setup.sh
    ├── farm-advisor-ui.jpeg
    └── README.md





## Run the Project Locally

  ### docker --> compose up --> build 
  
  ### Run Backend Only
    cd backend
    pip install -r requirements.txt
    uvicorn main:app --reload
    
  ### Run Frontend Only
    cd frontend
    npm install
    npm start

    ---
    

## Output

  * AI-generated crop/field analysis

  * Smart advisory insights

  * Improved decision-making for farmers
  


## Future Enhancements

  * Crop disease classification

  * Fertilizer & nutrient recommendation

  * Real-time weather-based advisory

  * Mobile application

  * Multi-language support for farmers




## Contribution

  Contributions are welcome!
  Fork this repository, create a new branch, and submit a pull request.

  

## Acknowledgements

 * Hugging Face 

 * FastAPI Community

 * Open-source ML models

 *  Farmers & agricultural researchers

   

## Author

 ### Rambhu Singh
 *  Full Stack Developer 
 *  AI & ML Enthusiast
 *  Passionate about building smart farming solutions
