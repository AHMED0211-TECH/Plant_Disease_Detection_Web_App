import { Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

export default function ProtectedRoute({ children }: any) {
  const { user, loading } = useAuth();

  // ✅ WAIT for session to load
  if (loading) {
    return <div>Loading...</div>;
  }

  // ✅ If not logged in → redirect
  if (!user) {
    return <Navigate to="/login" />;
  }

  return children;
}