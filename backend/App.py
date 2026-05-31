from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import torch
import torchvision.transforms as transforms
from CNN import CNN
from huggingface_hub import hf_hub_download

app = Flask(__name__)
CORS(app)  # allows frontend to connect

# ----------------------------
# 🔥 LOAD MODEL
# ----------------------------
MODEL_PATH = hf_hub_download(
    repo_id="Shuaib02/leafsense-model",
    filename="plant_disease_model_1_latest.pt"
)

device = torch.device("cpu")

model = CNN(39)  # change if your class count is different
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()

# ----------------------------
# 🖼️ IMAGE TRANSFORM
# ----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # change if your model uses different size
    transforms.ToTensor(),
])

# ----------------------------
# 🌿 CLASS NAMES (IMPORTANT)
# ----------------------------
classes = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Background_without_leaves",
    "Blueberry___healthy",
    "Cherry___Powdery_mildew",
    "Cherry___healthy",
    "Corn___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspbarry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
    
    # 👉 REPLACE with your actual 39 class names
]

# ----------------------------
# 🚀 API ROUTE
# ----------------------------
@app.route("/")
def home():
    return "Backend is running"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files["image"]

        # Open image
        image = Image.open(file).convert("RGB")
        image = transform(image).unsqueeze(0).to(device)

        # Predict
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)

        #result = int(predicted.item())
        result = classes[predicted.item()]

        return jsonify({
            "result": result
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
    


# ----------------------------
# 🏁 RUN SERVER
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)