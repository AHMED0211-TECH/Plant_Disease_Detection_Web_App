import { useParams, Link, useNavigate,useLocation } from "react-router-dom";
import { motion } from "framer-motion";
import { ArrowLeft, CheckCircle, AlertTriangle, ScanLine, Shield, Pill } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DashboardLayout } from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { getScanHistory } from "@/lib/mockData";

function ResultsContent() {
  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state?.result;
  const image = location.state?.image;

  console.log("Result:", result); // DEBUG

  if (!result) {
    return (
      <div className="text-center py-20">
        <p className="text-muted-foreground">Result not found</p>
        <Button
          variant="outline"
          className="mt-4"
          onClick={() => navigate("/scan")}
        >
          Scan a Plant
        </Button>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <button
          onClick={() => navigate(-1)}
          className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground mb-4"
        >
          <ArrowLeft className="h-4 w-4" /> Back
        </button>
        <h1 className="font-display text-2xl md:text-3xl font-bold">
          Scan Results
        </h1>
      </motion.div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Image */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="rounded-xl overflow-hidden border shadow-card"
        >
          {image && (
            <img
              src={image}
              alt="Scanned leaf"
              className="w-full h-64 object-cover"
            />
          )}
        </motion.div>

        {/* Result */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-card rounded-xl border shadow-card p-6 flex flex-col justify-center"
        >
          <h2 className="font-display text-2xl font-bold mb-2">
            🌿 {result}
          </h2>

          <p className="text-sm text-muted-foreground">
            This is the detected plant disease from the AI model.
          </p>
        </motion.div>
      </div>

      <Button
        className="w-full bg-gradient-primary text-primary-foreground gap-2"
        size="lg"
        onClick={() => navigate("/scan")}
      >
        <ScanLine className="h-5 w-5" /> Scan Another Plant
      </Button>
    </div>
  );
}
export default function Results() {
  const { isAuthenticated } = useAuth();
  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-background p-4 md:p-8">
        <ResultsContent />
      </div>
    );
  }
  return <DashboardLayout><ResultsContent /></DashboardLayout>;
}
