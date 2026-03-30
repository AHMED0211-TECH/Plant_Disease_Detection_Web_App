import { useState } from "react";
import { motion } from "framer-motion";
import { User, Lock, LogOut } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { DashboardLayout } from "@/components/DashboardLayout";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";
import { useNavigate } from "react-router-dom";

export default function Profile() {
  const { user, logout } = useAuth();
  const { toast } = useToast();
  const navigate = useNavigate();
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentPassword || !newPassword) {
      toast({ title: "Please fill in all fields", variant: "destructive" });
      return;
    }
    if (newPassword.length < 6) {
      toast({ title: "New password must be at least 6 characters", variant: "destructive" });
      return;
    }
    toast({ title: "Password updated successfully!" });
    setCurrentPassword("");
    setNewPassword("");
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <DashboardLayout>
      <div className="max-w-2xl mx-auto space-y-6">
        <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-2xl md:text-3xl font-bold">Profile</h1>
          <p className="text-muted-foreground mt-1">Manage your account settings</p>
        </motion.div>

        <div className="bg-card rounded-xl border shadow-card p-6">
          <div className="flex items-center gap-4 mb-6">
            <div className="h-16 w-16 rounded-full bg-primary/10 flex items-center justify-center">
              <User className="h-8 w-8 text-primary" />
            </div>
            <div>
              <h2 className="font-display font-semibold text-lg">{user?.name}</h2>
              <p className="text-sm text-muted-foreground">{user?.email}</p>
            </div>
          </div>
        </div>

        <div className="bg-card rounded-xl border shadow-card p-6">
          <div className="flex items-center gap-2 mb-4">
            <Lock className="h-5 w-5 text-primary" />
            <h3 className="font-display font-semibold text-lg">Change Password</h3>
          </div>
          <form onSubmit={handleChangePassword} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="current">Current Password</Label>
              <Input id="current" type="password" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} />
            </div>
            <div className="space-y-2">
              <Label htmlFor="new">New Password</Label>
              <Input id="new" type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
            </div>
            <Button type="submit" className="bg-gradient-primary text-primary-foreground">Update Password</Button>
          </form>
        </div>

        <Button variant="destructive" className="w-full gap-2" onClick={handleLogout}>
          <LogOut className="h-4 w-4" /> Sign Out
        </Button>
      </div>
    </DashboardLayout>
  );
}
