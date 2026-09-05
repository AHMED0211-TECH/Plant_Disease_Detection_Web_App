import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Leaf, Mail, Lock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";
import { supabase } from "@/lib/supabase";
import { motion } from "framer-motion";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!email || !password) {
      toast({ title: "Please fill in all fields", variant: "destructive" });
      return;
    }

    setLoading(true);

    try {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) throw error;

      toast({ title: "Login successful ✅" });
      navigate("/dashboard");
    } catch (error: any) {
      toast({ title: error.message || "Login failed", variant: "destructive" });
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
                placeholder="••••••••"
                className="pl-10 h-12 rounded-lg border border-green-300 bg-white/20 text-white placeholder-green-200 focus:outline-none focus:ring-2 focus:ring-green-400 shadow-sm transition-all"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>
          </div>

          <div className="flex justify-end">
            <Link to="/forgot-password" className="text-sm text-green-100 hover:text-white transition-colors">
              Forgot password?
            </Link>
          </div>

          <Button
            type="submit"
            className="w-full h-12 rounded-lg bg-gradient-to-r from-green-600 to-emerald-500 text-white font-semibold shadow-md hover:shadow-lg transition-transform transform hover:scale-[1.02] active:scale-[0.98]"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
          </Button>
        </form>

        {/* Divider */}
        <div className="mt-6 relative">
          <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-green-300/30" /></div>
          <div className="relative flex justify-center text-xs">
            <span className="bg-white/10 px-2 text-green-100">or</span>
          </div>
        </div>

        {/* Google Sign In */}
          <Button
            variant="outline"
            className="w-full mt-4 gap-2 h-12 rounded-lg bg-white/20 border border-green-300 text-white font-medium shadow-sm hover:bg-white/30 transition-all"
            onClick={async () => {
            const { error } = await supabase.auth.signInWithOAuth({
            provider: 'google',
            options: {
            redirectTo: 'https://leafsense-ai-phi.vercel.app/dashboard',
            },
          })
        if (error) toast({ title: error.message, variant: 'destructive' })
      }}
    >
          <svg className="h-4 w-4" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
          </svg>
          Continue with Google
        </Button>

        {/* Sign Up */}
        <p className="text-center text-sm text-green-100 mt-6">
          Don't have an account?{" "}
          <Link to="/signup" className="text-white hover:underline font-medium">
            Sign up
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
