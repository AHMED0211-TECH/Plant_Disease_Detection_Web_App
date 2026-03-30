import { useState } from "react";
import { Link } from "react-router-dom";
import { Leaf, Mail, ArrowLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useToast } from "@/hooks/use-toast";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const { toast } = useToast();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      toast({ title: "Please enter your email", variant: "destructive" });
      return;
    }
    setSent(true);
    toast({ title: "Reset link sent! Check your email." });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/30 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-6">
            <Leaf className="h-8 w-8 text-primary" />
            <span className="font-display text-2xl font-bold">LeafSense AI</span>
          </Link>
          <h1 className="font-display text-2xl font-bold">Reset your password</h1>
          <p className="text-muted-foreground text-sm mt-1">We'll send you a reset link</p>
        </div>
        <div className="bg-card rounded-xl shadow-card border p-6">
          {sent ? (
            <div className="text-center py-4">
              <div className="h-12 w-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <Mail className="h-6 w-6 text-primary" />
              </div>
              <p className="font-medium mb-2">Check your email</p>
              <p className="text-sm text-muted-foreground">We've sent a password reset link to {email}</p>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <Input id="email" type="email" placeholder="you@example.com" className="pl-10" value={email} onChange={(e) => setEmail(e.target.value)} />
                </div>
              </div>
              <Button type="submit" className="w-full bg-gradient-primary text-primary-foreground">Send Reset Link</Button>
            </form>
          )}
        </div>
        <Link to="/login" className="flex items-center justify-center gap-2 text-sm text-muted-foreground mt-6 hover:text-foreground">
          <ArrowLeft className="h-4 w-4" /> Back to sign in
        </Link>
      </div>
    </div>
  );
}
