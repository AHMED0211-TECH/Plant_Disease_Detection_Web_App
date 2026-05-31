import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Leaf, Mail, Lock, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/lib/supabase";
import { motion } from "framer-motion";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name || !email || !password) {
      toast({ title: "Please fill in all fields", variant: "destructive" });
      return;
    }

    if (password.length < 6) {
      toast({ title: "Password must be at least 6 characters", variant: "destructive" });
      return;
    }

    setLoading(true);

    try {
      const { error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: {
            full_name: name,
          },
        },
      });

      if (error) throw error;

      toast({ title: "Account created successfully ✅" });
      navigate("/dashboard");
    } catch (error: any) {
      toast({ title: error.message || "Signup failed", variant: "destructive" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-900 via-green-800 to-emerald-700 overflow-hidden p-4">
      {/* Decorative blurred blobs */}
      <div className="absolute -top-20 -left-20 w-72 h-72 bg-green-500 opacity-30 rounded-full blur-3xl" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-emerald-600 opacity-20 rounded-full blur-3xl" />
      <div className="absolute top-1/2 left-1/3 w-64 h-64 bg-green-400 opacity-20 rounded-full blur-2xl" />

      <motion.div
        initial={{ opacity: 0, y: 30, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.6 }}
        whileHover={{ scale: 1.02 }}
        className="relative z-10 w-full max-w-md rounded-2xl backdrop-blur-xl bg-white/10 border border-white/20 shadow-xl p-8"
      >
        {/* Branding */}
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-4">
            <div className="flex items-center justify-center w-14 h-14 rounded-full bg-gradient-to-tr from-green-600 to-emerald-500 shadow-md">
              <Leaf className="h-7 w-7 text-white" />
            </div>
            <span className="font-display text-2xl font-bold text-white">LeafSense AI</span>
          </Link>
          <p className="text-green-100 text-sm">AI-Powered Plant Disease Detection</p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="space-y-2">
            <Label htmlFor="name" className="text-green-100">Full Name</Label>
            <div className="relative">
              <User className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-green-200" />
              <Input
                id="name"
                placeholder="John Doe"
                className="pl-10 h-12 rounded-lg border border-green-300 bg-white/20 text-white placeholder-green-200 focus:outline-none focus:ring-2 focus:ring-green-400 shadow-sm transition-all"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email" className="text-green-100">Email</Label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-green-200" />
              <Input
                id="email"
                type="email"
                placeholder="you@example.com"
                className="pl-10 h-12 rounded-lg border border-green-300 bg-white/20 text-white placeholder-green-200 focus:outline-none focus:ring-2 focus:ring-green-400 shadow-sm transition-all"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password" className="text-green-100">Password</Label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-green-200" />
              <Input
                id="password"
                type="password"
                placeholder="Min 6 characters"
                className="pl-10 h-12 rounded-lg border border-green-300 bg-white/20 text-white placeholder-green-200 focus:outline-none focus:ring-2 focus:ring-green-400 shadow-sm transition-all"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <Button
            type="submit"
            className="w-full h-12 rounded-lg bg-gradient-to-r from-green-600 to-emerald-500 text-white font-semibold shadow-md hover:shadow-lg transition-transform transform hover:scale-[1.02] active:scale-[0.98]"
            disabled={loading}
          >
            {loading ? "Creating account..." : "Create Account"}
          </Button>
        </form>

        {/* Sign In Link */}
        <p className="text-center text-sm text-green-100 mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-white hover:underline font-medium">
            Sign in
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
