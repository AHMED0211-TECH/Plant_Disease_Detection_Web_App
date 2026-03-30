import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import { AuthProvider } from "@/contexts/AuthContext";
import Index from "./pages/Index";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import ForgotPassword from "./pages/ForgotPassword";
import Dashboard from "./pages/Dashboard";
import Scan from "./pages/Scan";
import Results from "./pages/Results";
import HistoryPage from "./pages/HistoryPage";
import Profile from "./pages/Profile";
import NotFound from "./pages/NotFound";
import ProtectedRoute from "./components/ProtectedRoute";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <AuthProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<Signup />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route
               path="/dashboard"
               element={
               <ProtectedRoute>
               <Dashboard />
                </ProtectedRoute>
              }
            />
            <Route
              path="/scan"
              element={
              <ProtectedRoute>
              <Scan/>
              </ProtectedRoute>
            }
          />
            <Route
              path="/results"
              element={
              <ProtectedRoute>
              <Results />
              </ProtectedRoute>
            }
          />
            <Route
              path="/history"
              element={
              <ProtectedRoute>
              <HistoryPage />
              </ProtectedRoute>
            }
          />
            <Route
              path="/profile"
              element={
              <ProtectedRoute>
              <Profile/>
              </ProtectedRoute>
            }
          />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </TooltipProvider>
  </QueryClientProvider>
);

export default App;
