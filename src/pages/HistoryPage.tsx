import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { Clock, ScanLine, AlertTriangle, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { DashboardLayout } from "@/components/DashboardLayout";
import { getScanHistory } from "@/lib/mockData";

export default function HistoryPage() {
  const history = getScanHistory();

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-2xl md:text-3xl font-bold">Scan History</h1>
          <p className="text-muted-foreground mt-1">Your previous plant diagnoses</p>
        </motion.div>

        {history.length === 0 ? (
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
                  <img src={scan.imageUrl} alt={scan.diseaseName} className="h-16 w-16 rounded-lg object-cover shrink-0" />
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
                      <span>{new Date(scan.date).toLocaleDateString()} {new Date(scan.date).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</span>
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
