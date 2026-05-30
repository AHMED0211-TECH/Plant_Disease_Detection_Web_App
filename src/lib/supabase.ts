import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://vfrgfqtleewqwpqbgxji.supabase.co";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZmcmdmcXRsZWV3cXdwcWJneGppIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAwOTI5NjgsImV4cCI6MjA5NTY2ODk2OH0.bLzjBP6hs-2xdpcMy5UJjz_bIx6vYQY7aH7eIlfZrCk";

export const supabase = createClient(supabaseUrl, supabaseKey);