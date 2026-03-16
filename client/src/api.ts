const BASE_URL = import.meta.env.DEV ? "http://localhost:4001" : "";

export async function fetchApi<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, options);
  if (!res.ok) throw new Error(`API Error: ${res.status}`);
  return res.json();
}
