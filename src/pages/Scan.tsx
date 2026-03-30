import { useState, useRef, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Upload, Camera, X, Loader2, ScanLine, Leaf } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DashboardLayout } from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { getRandomDiagnosis, addScanToHistory, type ScanResult } from "@/lib/mockData";
import { useToast } from "@/hooks/use-toast";

function ScanContent() {
  const [image, setImage] = useState<string | null>(null);
  const [fileName, setFileName] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();
  const { toast } = useToast();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [result, setResult] = useState("");


  const handleFile = useCallback((file: File) => {
    if (!file.type.startsWith("image/")) {
      toast({ title: "Please upload an image file", variant: "destructive" });
      return;
    }
    setSelectedFile(file);
    setFileName(file.name);
    const reader = new FileReader();
    reader.onload = (e) => setImage(e.target?.result as string);
    reader.readAsDataURL(file);
  }, [toast]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) handleFile(file);
  }, [handleFile]);

 const handleAnalyze = async () => {
  if (!selectedFile) {
    console.log("No file selected");
    return;
  }

  setAnalyzing(true);

  const formData = new FormData();
  formData.append("image", selectedFile);

  try {
    const res = await fetch("http://127.0.0.1:5001/predict", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log("Backend response:", data);

    //setResult(data.result);
    console.log("Navigating with:", data.result);
    
    navigate("/results", {
    state: {
    result: data.result,
    image: image
  }
});

    setAnalyzing(false);
  } catch (error) {
    console.error("Error:", error);
    setAnalyzing(false);
  }
};

  const handleCameraCapture = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.capture = "environment";
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) handleFile(file);
    };
    input.click();
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="font-display text-2xl md:text-3xl font-bold">Scan Your Plant</h1>
        <p className="text-muted-foreground mt-1">Upload or capture a photo of a plant leaf</p>
      </motion.div>

      <AnimatePresence mode="wait">
        {!image ? (
          <motion.div
            key="upload"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className={`border-2 border-dashed rounded-xl p-10 text-center transition-colors ${
              dragOver ? "border-primary bg-primary/5" : "border-border"
            }`}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
          >
            <Upload className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
            <p className="font-medium mb-2">Drag & drop your image here</p>
            <p className="text-sm text-muted-foreground mb-6">or use the buttons below</p>
            <div className="flex flex-wrap justify-center gap-3">
              <Button variant="outline" className="gap-2" onClick={() => fileRef.current?.click()}>
                <Upload className="h-4 w-4" /> Upload Image
              </Button>
              <Button variant="outline" className="gap-2" onClick={handleCameraCapture}>
                <Camera className="h-4 w-4" /> Use Camera
              </Button>
            </div>
            <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])} />
          </motion.div>
        ) : (
          <motion.div key="preview" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="space-y-4">
            <div className="relative rounded-xl overflow-hidden border shadow-card">
              <img src={image} alt="Plant leaf preview" className="w-full max-h-96 object-contain bg-muted/30" />
              <button
                onClick={() => { setImage(null); setFileName(""); }}
                className="absolute top-3 right-3 bg-card/80 backdrop-blur rounded-full p-1.5 shadow-md hover:bg-card"
              >
                <X className="h-4 w-4" />
              </button>
              {analyzing && (
                <div className="absolute inset-0 bg-foreground/50 flex flex-col items-center justify-center">
                  <div className="bg-card rounded-xl p-6 shadow-lg text-center">
                    <Loader2 className="h-10 w-10 text-primary animate-spin mx-auto mb-3" />
                    <p className="font-display font-semibold">Analyzing leaf with AI...</p>
                    <p className="text-sm text-muted-foreground mt-1">This may take a few seconds</p>
                    <div className="mt-4 h-1.5 bg-muted rounded-full overflow-hidden w-48">
                      <motion.div
                        className="h-full bg-gradient-primary rounded-full"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 2.5, ease: "easeInOut" }}
                      />
                    </div>
                  </div>
                </div>
              )}
            </div>
            <p className="text-sm text-muted-foreground">{fileName}</p>
            <Button
              className="w-full bg-gradient-primary text-primary-foreground gap-2"
              size="lg"
              onClick={handleAnalyze}
              disabled={analyzing}
            >
              <ScanLine className="h-5 w-5" /> Detect Disease
            </Button>
            
            {result && (
  <div className="mt-4 text-lg font-semibold">
    Result: {result}
  </div>
)}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

// Wrapper that handles demo mode (no auth required)
export default function Scan() {
  const [searchParams] = useSearchParams();
  const isDemo = searchParams.get("demo") === "true";
  const { isAuthenticated } = useAuth();

  if (isDemo || !isAuthenticated) {
    // Demo mode: render without sidebar
    return (
      <div className="min-h-screen bg-background">
        <nav className="border-b">
          <div className="container mx-auto flex items-center gap-2 h-14 px-4">
            <Leaf className="h-6 w-6 text-primary" />
            <span className="font-display font-bold">LeafSense AI — Demo Mode</span>
          </div>
        </nav>
        <div className="p-4 md:p-8">
          <ScanContent />
        </div>
      </div>
    );
  }

  return (
    <DashboardLayout>
      <ScanContent />
    </DashboardLayout>
  );
}
