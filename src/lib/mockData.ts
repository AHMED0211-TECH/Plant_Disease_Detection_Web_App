export interface ScanResult {
  id: string;
  imageUrl: string;
  diseaseName: string;
  confidence: number;
  description: string;
  treatment: string[];
  prevention: string[];
  date: string;
  isHealthy: boolean;
}

const diseases: Omit<ScanResult, "id" | "imageUrl" | "date">[] = [
  {
    diseaseName: "Tomato Late Blight",
    confidence: 94.7,
    description: "Late blight is caused by the oomycete pathogen Phytophthora infestans. It can devastate tomato and potato crops within days under favorable conditions.",
    treatment: [
      "Apply copper-based fungicides immediately",
      "Remove and destroy infected plant parts",
      "Use chlorothalonil or mancozeb-based fungicides",
      "Ensure proper air circulation around plants",
    ],
    prevention: [
      "Plant resistant varieties when possible",
      "Avoid overhead watering",
      "Ensure proper spacing between plants",
      "Monitor weather conditions for blight-favorable conditions",
    ],
    isHealthy: false,
  },
  {
    diseaseName: "Apple Scab",
    confidence: 91.2,
    description: "Apple scab is caused by the fungus Venturia inaequalis. It affects leaves and fruit, causing dark, scabby lesions.",
    treatment: [
      "Apply fungicide sprays during wet spring weather",
      "Remove fallen leaves in autumn",
      "Prune trees to improve air circulation",
    ],
    prevention: [
      "Plant scab-resistant apple varieties",
      "Maintain good sanitation practices",
      "Apply preventive fungicide in early spring",
    ],
    isHealthy: false,
  },
  {
    diseaseName: "Healthy Plant",
    confidence: 97.3,
    description: "This plant appears to be in excellent health with no visible signs of disease, pest damage, or nutrient deficiency.",
    treatment: ["No treatment needed — continue regular care"],
    prevention: [
      "Maintain regular watering schedule",
      "Ensure proper nutrition and fertilization",
      "Monitor regularly for early signs of disease",
    ],
    isHealthy: true,
  },
  {
    diseaseName: "Powdery Mildew",
    confidence: 88.5,
    description: "Powdery mildew is a fungal disease that forms a white powdery coating on leaf surfaces, reducing photosynthesis.",
    treatment: [
      "Apply neem oil or sulfur-based fungicide",
      "Remove heavily infected leaves",
      "Improve air circulation around plants",
    ],
    prevention: [
      "Avoid overcrowding plants",
      "Water at the base, not overhead",
      "Choose resistant varieties",
    ],
    isHealthy: false,
  },
];

export function getRandomDiagnosis(): Omit<ScanResult, "id" | "imageUrl" | "date"> {
  return diseases[Math.floor(Math.random() * diseases.length)];
}

export function getScanHistory(): ScanResult[] {
  const stored = localStorage.getItem("leafsense_history");
  return stored ? JSON.parse(stored) : [];
}

export function addScanToHistory(scan: ScanResult) {
  const history = getScanHistory();
  history.unshift(scan);
  localStorage.setItem("leafsense_history", JSON.stringify(history));
}

export function getStats() {
  const history = getScanHistory();
  return {
    totalScans: history.length,
    diseasesDetected: history.filter((s) => !s.isHealthy).length,
    healthyPlants: history.filter((s) => s.isHealthy).length,
  };
}
