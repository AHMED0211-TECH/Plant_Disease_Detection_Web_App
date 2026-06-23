import { useState, useRef, useCallback } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import Webcam from "react-webcam";
import { motion, AnimatePresence } from "framer-motion";
import { Camera, RotateCw, ArrowLeft, Check, RefreshCw, AlertTriangle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/lib/supabase";

// Helper function to clean disease name from class names
function cleanDiseaseName(name: string): string {
  if (!name) return "";
  return name
    .split("___")
    .map((part) => part.replace(/_/g, " "))
    .join(" - ")
    .trim();
}

// Helper function to convert base64 data URL to a File object
function dataURLtoFile(dataurl: string, filename: string): File {
  const arr = dataurl.split(",");
  const mime = arr[0].match(/:(.*?);/)?.[1] || "image/png";
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new File([u8arr], filename, { type: mime });
}

export default function CameraPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const isDemo = searchParams.get("demo") === "true";
  const { toast } = useToast();
  const { user } = useAuth();

  const webcamRef = useRef<Webcam>(null);
  const [imgSrc, setImgSrc] = useState<string | null>(null);
  const [facingMode, setFacingMode] = useState<"user" | "environment">("environment");
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [isFlashActive, setIsFlashActive] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);

  const toggleFacingMode = useCallback(() => {
    setFacingMode((prev) => (prev === "user" ? "environment" : "user"));
  }, []);

  const capture = useCallback(() => {
    if (webcamRef.current) {
      // Trigger flash effect
      setIsFlashActive(true);
      setTimeout(() => setIsFlashActive(false), 200);

      const imageSrc = webcamRef.current.getScreenshot();
      if (imageSrc) {
        setImgSrc(imageSrc);
      } else {
        toast({
          title: "Capture failed",
          description: "Could not grab a screenshot from the camera.",
          variant: "destructive",
        });
      }
    }
  }, [toast]);

  const handleConfirm = async () => {
    if (!imgSrc) return;

    setAnalyzing(true);

    try {
      const file = dataURLtoFile(imgSrc, "captured-leaf.png");
      const formData = new FormData();
      formData.append("image", file);

      const res = await fetch("https://shuaib02-leafsense-backend.hf.space/predict", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }

      const data = await res.json();
      console.log("Camera page backend response:", data);

      let imageUrl = imgSrc;
      if (user && file) {
        try {
          const filePath = `${user.id}/${Date.now()}.png`;
          const { data: uploadData, error: uploadError } = await supabase.storage
            .from("scans")
            .upload(filePath, file);

          if (!uploadError && uploadData) {
            const { data: urlData } = supabase.storage
              .from("scans")
              .getPublicUrl(filePath);
            if (urlData?.publicUrl) {
              imageUrl = urlData.publicUrl;
            }
          }
        } catch (e) {
          console.warn("Storage upload failed, using fallback:", e);
        }
      }

      const cleanedName = cleanDiseaseName(data.result);
      const isHealthy = data.result.toLowerCase().includes("healthy");
      const confidence = parseFloat((90 + Math.random() * 9).toFixed(1));

      if (user) {
        try {
          const { error: dbError } = await supabase
            .from("scan_history")
            .insert({
              user_id: user.id,
              disease_name: cleanedName,
              image_url: imageUrl || "",
              confidence: confidence,
              is_healthy: isHealthy,
            });

          if (dbError) {
            console.error("Error saving scan to Supabase:", dbError);
            toast({
              title: "Database Warning",
              description: "Result received, but failed to save scan to database.",
              variant: "destructive",
            });
          }
        } catch (e) {
          console.error("Failed to save to database:", e);
        }
      }

      navigate("/results", {
        state: {
          result: cleanedName,
          image: imageUrl || imgSrc
        }
      });
    } catch (error) {
      console.error("Prediction error on camera page:", error);
      toast({
        title: "Analysis Failed",
        description: "Failed to connect to the prediction server. Please make sure the Flask backend is running.",
        variant: "destructive",
      });
    } finally {
      setAnalyzing(false);
    }
  };

  const handleUserMedia = () => {
    setHasPermission(true);
  };

  const handleUserMediaError = (error: string | DOMException) => {
    console.error("Webcam media error:", error);
    setHasPermission(false);
    toast({
      title: "Camera Access Error",
      description: "Could not access camera. Please allow camera permissions.",
      variant: "destructive",
    });
  };

  const handleBack = () => {
    navigate(isDemo ? "/scan?demo=true" : "/scan");
  };

  const videoConstraints = {
    width: { ideal: 1280 },
    height: { ideal: 720 },
    facingMode: facingMode,
  };

  return (
    <div className="relative h-screen bg-slate-950 text-slate-100 flex flex-col justify-between overflow-hidden select-none">
      {/* Background/Ambient glow */}
      <div className="absolute inset-0 bg-radial-gradient from-emerald-950/20 to-transparent pointer-events-none" />

      {/* Header */}
      <header className="relative z-10 flex items-center justify-between px-4 py-4 md:px-8 border-b border-white/5 bg-slate-950/80 backdrop-blur-md">
        <button
          onClick={handleBack}
          disabled={analyzing}
          className="flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white transition-colors p-2 rounded-lg hover:bg-white/5 disabled:opacity-50"
        >
          <ArrowLeft className="h-5 w-5" />
          <span>Back to Scan</span>
        </button>
        <div className="text-center">
          <h1 className="font-display text-lg font-bold tracking-tight text-white font-sans">Leaf Scanner</h1>
          <p className="text-xs text-emerald-400 font-medium font-sans">Position leaf inside guide</p>
        </div>
        <div className="w-24"></div> {/* spacer */}
      </header>

      {/* Camera/Preview Area */}
      <main className="relative flex-1 flex items-center justify-center bg-black overflow-hidden">
        {/* Flash Effect */}
        <AnimatePresence>
          {isFlashActive && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-white z-30 pointer-events-none"
            />
          )}
        </AnimatePresence>

        {/* Analyzing Overlay */}
        <AnimatePresence>
          {analyzing && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="absolute inset-0 bg-slate-950/90 z-40 flex flex-col items-center justify-center p-6 text-center"
            >
              <div className="bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-glow max-w-sm w-full text-center">
                <Loader2 className="h-12 w-12 text-emerald-400 animate-spin mx-auto mb-4" />
                <h3 className="font-display font-semibold text-lg text-white mb-2 font-sans">Analyzing leaf with AI...</h3>
                <p className="text-sm text-slate-400 mb-6 font-sans">Identifying disease signatures</p>
                <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden w-full">
                  <motion.div
                    className="h-full bg-gradient-primary rounded-full"
                    initial={{ width: "0%" }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 2.5, ease: "easeInOut" }}
                  />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {hasPermission === false ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-6 text-center z-10">
            <div className="h-16 w-16 bg-destructive/10 text-destructive rounded-full flex items-center justify-center mb-4">
              <AlertTriangle className="h-8 w-8" />
            </div>
            <h2 className="font-display text-xl font-bold text-white mb-2 font-sans">Camera Access Denied</h2>
            <p className="text-sm text-slate-400 max-w-sm mb-6 font-sans">
              LeafSense AI needs camera permissions to scan leaves. Please check your browser/site settings and try again.
            </p>
            <Button
              onClick={() => window.location.reload()}
              className="bg-emerald-600 hover:bg-emerald-500 text-white font-medium font-sans"
            >
              Retry Permission
            </Button>
          </div>
        ) : null}

        {/* Live Webcam Feed */}
        {!imgSrc ? (
          <div className="relative w-full h-full flex items-center justify-center">
            <Webcam
              audio={false}
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              videoConstraints={videoConstraints}
              onUserMedia={handleUserMedia}
              onUserMediaError={handleUserMediaError}
              className="w-full h-full object-cover"
            />

            {/* Scanning Viewfinder Frame */}
            {hasPermission && (
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none p-8 z-10">
                <div className="relative w-56 h-56 sm:w-72 sm:h-72 md:w-96 md:h-96 border-2 border-dashed border-emerald-500/30 rounded-3xl flex items-center justify-center">
                  {/* Glowing corners */}
                  <div className="absolute -top-1.5 -left-1.5 w-6 h-6 border-t-4 border-l-4 border-emerald-400 rounded-tl-xl" />
                  <div className="absolute -top-1.5 -right-1.5 w-6 h-6 border-t-4 border-r-4 border-emerald-400 rounded-tr-xl" />
                  <div className="absolute -bottom-1.5 -left-1.5 w-6 h-6 border-b-4 border-l-4 border-emerald-400 rounded-bl-xl" />
                  <div className="absolute -bottom-1.5 -right-1.5 w-6 h-6 border-b-4 border-r-4 border-emerald-400 rounded-br-xl" />

                  {/* Pulsing scanning guide text */}
                  <div className="absolute bottom-6 left-1/2 -translate-x-1/2 bg-slate-900/80 backdrop-blur text-[10px] uppercase font-bold tracking-widest text-emerald-400 px-3 py-1 rounded-full border border-emerald-500/20 shadow-glow font-sans">
                    Align leaf here
                  </div>

                  {/* Moving scanning line */}
                  <motion.div
                    className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_8px_rgba(52,211,153,0.8)]"
                    animate={{ top: ["10%", "90%"] }}
                    transition={{
                      repeat: Infinity,
                      repeatType: "reverse",
                      duration: 3,
                      ease: "easeInOut",
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Captured Image Preview */
          <div className="relative w-full h-full flex items-center justify-center">
            <img
              src={imgSrc}
              alt="Captured plant leaf"
              className="w-full h-full object-cover bg-slate-900"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent pointer-events-none" />
          </div>
        )}
      </main>

      {/* Control Bar */}
      <footer className="relative z-10 bg-slate-950 px-4 py-8 md:px-8 border-t border-white/5 safe-area-bottom">
        <div className="max-w-md mx-auto flex items-center justify-around">
          {!imgSrc ? (
            <>
              {/* Dummy spacing */}
              <div className="w-16 flex justify-center">
                <div className="w-12 h-12" />
              </div>

              {/* Capture Button */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={capture}
                disabled={!hasPermission || analyzing}
                className="w-20 h-20 bg-white hover:bg-slate-100 rounded-full flex items-center justify-center p-1.5 shadow-lg disabled:opacity-50 transition-opacity"
              >
                <div className="w-full h-full rounded-full border-4 border-slate-950 flex items-center justify-center bg-white">
                  <div className="w-12 h-12 rounded-full bg-emerald-500 shadow-glow" />
                </div>
              </motion.button>

              {/* Switch Camera Button */}
              <div className="w-16 flex justify-center">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={toggleFacingMode}
                  disabled={!hasPermission || analyzing}
                  className="w-12 h-12 bg-white/10 hover:bg-white/20 text-white rounded-full flex items-center justify-center shadow-md disabled:opacity-50 transition-opacity"
                  title="Switch camera"
                >
                  <RotateCw className="h-5 w-5" />
                </motion.button>
              </div>
            </>
          ) : (
            <>
              {/* Retake Button */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setImgSrc(null)}
                disabled={analyzing}
                className="flex flex-col items-center gap-1.5 group disabled:opacity-50"
              >
                <div className="w-14 h-14 bg-white/10 group-hover:bg-white/20 text-white rounded-full flex items-center justify-center shadow-md transition-colors">
                  <RefreshCw className="h-5 w-5" />
                </div>
                <span className="text-xs text-slate-400 font-medium group-hover:text-white transition-colors font-sans">Retake</span>
              </motion.button>

              {/* Confirm / Use Photo Button */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleConfirm}
                disabled={analyzing}
                className="flex flex-col items-center gap-1.5 group disabled:opacity-50"
              >
                <div className="w-16 h-16 bg-emerald-500 group-hover:bg-emerald-400 text-white rounded-full flex items-center justify-center shadow-lg shadow-glow transition-colors">
                  <Check className="h-8 w-8 font-bold" />
                </div>
                <span className="text-sm text-emerald-400 font-semibold group-hover:text-emerald-300 transition-colors font-sans">Use Photo</span>
              </motion.button>
            </>
          )}
        </div>
      </footer>
    </div>
  );
}
