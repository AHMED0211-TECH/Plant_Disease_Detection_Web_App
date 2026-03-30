import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Leaf, ScanLine, Zap, Target, Camera, ArrowRight, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import heroImage from "@/assets/hero-plant.jpg";

const features = [
  { icon: ScanLine, title: "AI Disease Detection", desc: "Advanced deep learning models identify 50+ plant diseases from a single photo" },
  { icon: Camera, title: "Camera Scan", desc: "Use your phone camera to scan leaves directly in the field" },
  { icon: Zap, title: "Instant Results", desc: "Get diagnosis and treatment recommendations in under 3 seconds" },
  { icon: Target, title: "98% Accuracy", desc: "Trained on millions of images for industry-leading precision" },
];

const steps = [
  { num: "01", title: "Upload or Capture", desc: "Take a photo of the affected leaf or upload from your gallery" },
  { num: "02", title: "AI Analysis", desc: "Our model analyzes the leaf patterns, color, and texture for disease markers" },
  { num: "03", title: "Get Treatment Plan", desc: "Receive disease identification, confidence score, and actionable treatment steps" },
];

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5 } }),
};

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <nav className="fixed top-0 w-full z-50 glass border-b">
        <div className="container mx-auto flex items-center justify-between h-16 px-4">
          <Link to="/" className="flex items-center gap-2">
            <Leaf className="h-7 w-7 text-primary" />
            <span className="font-display text-xl font-bold">LeafSense AI</span>
          </Link>
          <div className="flex items-center gap-3">
            <Link to="/login">
              <Button variant="ghost" size="sm">Log in</Button>
            </Link>
            <Link to="/signup">
              <Button size="sm" className="bg-gradient-primary text-primary-foreground">Get Started</Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-32 pb-20 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-secondary/50 via-background to-background" />
        <div className="container mx-auto px-4 relative z-10">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div initial="hidden" animate="visible" variants={fadeUp} custom={0}>
              <div className="inline-flex items-center gap-2 bg-primary/10 text-primary rounded-full px-4 py-1.5 text-sm font-medium mb-6">
                <Leaf className="h-4 w-4" /> AI-Powered Plant Care
              </div>
              <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
                Detect Plant Diseases{" "}
                <span className="text-gradient">in Seconds</span>{" "}
                using AI
              </h1>
              <p className="text-lg text-muted-foreground mb-8 max-w-lg">
                Upload a photo of any plant leaf and get instant AI-powered disease diagnosis with treatment recommendations.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link to="/scan?demo=true">
                  <Button size="lg" variant="outline" className="gap-2">
                    <ScanLine className="h-4 w-4" /> Try Demo
                  </Button>
                </Link>
                <Link to="/signup">
                  <Button size="lg" className="bg-gradient-primary text-primary-foreground gap-2">
                    Get Started <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="relative"
            >
              <div className="rounded-2xl overflow-hidden shadow-card-hover">
                <img src={heroImage} alt="Healthy plant leaves with dew drops" className="w-full h-auto object-cover" />
              </div>
              <div className="absolute -bottom-4 -left-4 bg-card rounded-xl p-4 shadow-card border flex items-center gap-3">
                <div className="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                  <CheckCircle className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="text-sm font-semibold">Healthy Plant</p>
                  <p className="text-xs text-muted-foreground">97.3% confidence</p>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={0} className="text-center mb-14">
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">Why LeafSense AI?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">Everything you need to keep your plants healthy and thriving</p>
          </motion.div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                custom={i}
                className="bg-card rounded-xl p-6 shadow-card border hover:shadow-card-hover transition-shadow duration-300"
              >
                <div className="h-12 w-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                  <f.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="font-display font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-sm text-muted-foreground">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <motion.div initial="hidden" whileInView="visible" viewport={{ once: true }} variants={fadeUp} custom={0} className="text-center mb-14">
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">Three simple steps to diagnose your plant</p>
          </motion.div>
          <div className="grid md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            {steps.map((s, i) => (
              <motion.div
                key={s.num}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                custom={i}
                className="text-center"
              >
                <div className="text-5xl font-display font-extrabold text-gradient mb-4">{s.num}</div>
                <h3 className="font-display font-semibold text-xl mb-2">{s.title}</h3>
                <p className="text-sm text-muted-foreground">{s.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="bg-gradient-hero rounded-2xl p-10 md:p-16 text-center">
            <h2 className="font-display text-3xl md:text-4xl font-bold text-primary-foreground mb-4">
              Start Protecting Your Plants Today
            </h2>
            <p className="text-primary-foreground/80 mb-8 max-w-lg mx-auto">
              Join thousands of farmers and gardeners using AI to keep their crops healthy.
            </p>
            <Link to="/signup">
              <Button size="lg" variant="secondary" className="gap-2 font-semibold">
                Get Started Free <ArrowRight className="h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Leaf className="h-5 w-5 text-primary" />
            <span className="font-display font-semibold">LeafSense AI</span>
          </div>
          <p className="text-sm text-muted-foreground">© 2026 LeafSense AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
