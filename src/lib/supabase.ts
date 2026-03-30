import { createClient } from "@supabase/supabase-js";

const supabaseUrl = "https://leeznrnkyvvxeyaqhxbu.supabase.co";
const supabaseKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxlZXpucm5reXZ2eGV5YXFoeGJ1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQwMDMxOTUsImV4cCI6MjA4OTU3OTE5NX0.d2Pu1-u2JN_GeSI19NJyte0HjksV-hqUuw5TsNV5Tyk";

export const supabase = createClient(supabaseUrl, supabaseKey);