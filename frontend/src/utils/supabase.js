import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabasePublishableKey = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;

export const supabase =
  supabaseUrl && supabasePublishableKey
    ? createClient(supabaseUrl, supabasePublishableKey)
    : null;

const PAGE_SIZE = 1000;

export async function fetchAllRows(tableName) {
  if (!supabase) {
    throw new Error(
      "Supabase is not configured. Set VITE_SUPABASE_URL and VITE_SUPABASE_PUBLISHABLE_KEY in the deployment environment."
    );
  }

  const rows = [];
  let offset = 0;

  while (true) {
    const { data, error } = await supabase
      .from(tableName)
      .select("*")
      .range(offset, offset + PAGE_SIZE - 1);

    if (error) {
      throw new Error(`Unable to load the "${tableName}" table: ${error.message}`);
    }

    rows.push(...data);
    if (data.length < PAGE_SIZE) {
      return rows;
    }

    offset += data.length;
  }
}
