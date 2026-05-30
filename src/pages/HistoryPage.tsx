import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Clock, ScanLine, AlertTriangle, CheckCircle, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DashboardLayout } from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { supabase } from "@/lib/supabase";

interface MappedScan {
  id: string;
  imageUrl: string;
  diseaseName: string;
  confidence: number;
  isHealthy: boolean;
  date: string;
}

export default function HistoryPage() {
  const { user } = useAuth();
  const [history, setHistory] = useState<MappedScan[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchHistory() {
      if (!user) {
        setLoading(false);
        return;
      }
      try {
        const { data, error } = await supabase
          .from("scan_history")
          .select("*")
          .eq("user_id", user.id)
          .order("created_at", { ascending: false });

        if (error) {
          console.error("Error fetching history from Supabase:", error);
        } else if (data) {
          const mapped: MappedScan[] = data.map((item: any) => ({
            id: item.id,
            imageUrl: item.image_url,
            diseaseName: item.disease_name,
            confidence: item.confidence,
            isHealthy: item.is_healthy,
            date: item.created_at,
          }));
          setHistory(mapped);
        }
      } catch (err) {
        console.error("Failed to query scan history:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchHistory();
  }, [user]);

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-2xl md:text-3xl font-bold">Scan History</h1>
          <p className="text-muted-foreground mt-1">Your previous plant diagnoses</p>
        </motion.div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20">
            <Loader2 className="h-10 w-10 text-primary animate-spin mb-4" />
            <p className="text-sm text-muted-foreground">Loading your scan history...</p>
          </div>
        ) : history.length === 0 ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center py-20">
            <Clock className="h-16 w-16 text-muted-foreground/30 mx-auto mb-4" />
            <h3 className="font-display font-semibold text-lg mb-2">No scans yet</h3>
            <p className="text-sm text-muted-foreground mb-6">Start by scanning your first plant</p>
            <Link to="/scan">
              <Button className="bg-gradient-primary text-primary-foreground gap-2">
                <ScanLine className="h-4 w-4" /> Scan a Plant
              </Button>
            </Link>
          </motion.div>
        ) : (
          <div className="space-y-3">
            {history.map((scan, i) => (
              <motion.div
                key={scan.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <Link
                  to={`/results/${scan.id}`}
                  className="flex items-center gap-4 bg-card rounded-xl border shadow-card p-4 hover:shadow-card-hover transition-shadow"
                >
                  <img src={scan.imageUrl} alt={scan.diseaseName} className="h-16 w-16 rounded-lg object-cover shrink-0 bg-muted/10" />
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      {scan.isHealthy ? (
                        <CheckCircle className="h-4 w-4 text-success shrink-0" />
                      ) : (
                        <AlertTriangle className="h-4 w-4 text-warning shrink-0" />
                      )}
                      <span className="font-medium truncate">{scan.diseaseName}</span>
                    </div>
                    <div className="flex items-center gap-4 text-sm text-muted-foreground">
                      <span>{scan.confidence}% confidence</span>
                      <span>
                        {new Date(scan.date).toLocaleDateString()} {new Date(scan.date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </span>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
