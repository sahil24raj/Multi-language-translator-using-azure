export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");

  if (req.method === "OPTIONS") {
    return res.status(204).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Use POST /api/translate with a JSON body." });
  }

  const { endpoint, key, region, text, targets } = req.body || {};

  if (!endpoint || !key || !text || !Array.isArray(targets) || targets.length === 0) {
    return res.status(400).json({ error: "endpoint, key, text, and targets are required." });
  }

  // Remove any spaces, newlines, or invisible characters that sometimes copy over from Azure portal
  const cleanKey = String(key).replace(/[\s\u200B-\u200D\uFEFF]/g, '');
  const cleanRegion = String(region).replace(/[\s\u200B-\u200D\uFEFF]/g, '');

  const baseEndpoint = String(endpoint).trim().replace(/\/+$/, "");
  const query = new URLSearchParams({ "api-version": "3.0" });
  for (const lang of targets) {
    query.append("to", String(lang));
  }

  const translatorUrl = `${baseEndpoint}/translate?${query.toString()}`;

  const headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": cleanKey,
    "X-ClientTraceId": Math.random().toString(36).substring(2) + Date.now().toString(36)
  };

  if (cleanRegion) {
    headers["Ocp-Apim-Subscription-Region"] = cleanRegion;
  }

  try {
    const upstream = await fetch(translatorUrl, {
      method: "POST",
      headers,
      body: JSON.stringify([{ text: String(text) }])
    });

    const bodyText = await upstream.text();
    let bodyJson;

    try {
      bodyJson = JSON.parse(bodyText);
    } catch {
      bodyJson = null;
    }

    if (!upstream.ok) {
      const errorMessage = bodyJson?.error?.message || bodyText || `Azure error ${upstream.status}`;
      return res.status(upstream.status).json({ error: errorMessage });
    }

    const translations = {};
    const items = Array.isArray(bodyJson) && bodyJson[0] ? bodyJson[0].translations || [] : [];

    for (const item of items) {
      if (item?.to) {
        translations[item.to] = item.text;
      }
    }

    return res.status(200).json({ translations });
  } catch (err) {
    return res.status(502).json({ error: `Unable to reach Azure endpoint: ${err.message}` });
  }
}
