import { motion } from "framer-motion";
import { ScanLine, History, Leaf, Activity, ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { DashboardLayout } from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { getStats } from "@/lib/mockData";

export default function Dashboard() {
  const { user } = useAuth();
  const stats = getStats();

  const cards = [
    { label: "Total Scans", value: stats.totalScans, icon: ScanLine, color: "text-primary" },
    { label: "Diseases Detected", value: stats.diseasesDetected, icon: Activity, color: "text-destructive" },
    { label: "Healthy Plants", value: stats.healthyPlants, icon: Leaf, color: "text-success" },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-2xl md:text-3xl font-bold">
            Welcome back, {user?.name || "User"} 👋
          </h1>
          <p className="text-muted-foreground mt-1">Here's your plant health overview</p>
        </motion.div>

        <div className="grid sm:grid-cols-3 gap-4">
          {cards.map((c, i) => (
            <motion.div
              key={c.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-card rounded-xl border shadow-card p-6"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-muted-foreground">{c.label}</span>
                <c.icon className={`h-5 w-5 ${c.color}`} />
              </div>
              <p className="font-display text-3xl font-bold">{c.value}</p>
            </motion.div>
          ))}
        </div>

        <div className="grid sm:grid-cols-2 gap-4">
          <Link to="/scan">
            <div className="bg-gradient-primary rounded-xl p-6 text-primary-foreground hover:opacity-90 transition-opacity cursor-pointer">
              <ScanLine className="h-8 w-8 mb-3" />
              <h3 className="font-display font-semibold text-lg mb-1">Scan New Plant</h3>
              <p className="text-sm opacity-80 mb-4">Upload or capture a leaf image for instant diagnosis</p>
              <span className="inline-flex items-center gap-1 text-sm font-medium">
                Start scan <ArrowRight className="h-4 w-4" />
              </span>
            </div>
          </Link>
          <Link to="/history">
            <div className="bg-card rounded-xl border shadow-card p-6 hover:shadow-card-hover transition-shadow cursor-pointer">
              <History className="h-8 w-8 mb-3 text-primary" />
              <h3 className="font-display font-semibold text-lg mb-1">View History</h3>
              <p className="text-sm text-muted-foreground mb-4">Browse your previous scan results and treatments</p>
              <span className="inline-flex items-center gap-1 text-sm font-medium text-primary">
                View all <ArrowRight className="h-4 w-4" />
              </span>
            </div>
          </Link>
        </div>
      </div>
    </DashboardLayout>
  );
}
