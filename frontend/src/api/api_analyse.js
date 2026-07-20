import axios from "axios";

// const BASE_URL = "http://localhost:8000";
const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
/**
 * Détecter les noyaux dans le fichier en cache
 */
export async function detecterNoyaux(config = {}) {
  const response = await axios.post(`${BASE_URL}/analyse/detecter_noyaux`, {
    methode:       config.methode       ?? "threshold",
    projection:    config.projection    ?? "max",
    surface_min:   config.surface_min   ?? 500,
    surface_max:   config.surface_max   ?? 50000,
    rondeur_seuil: config.rondeur_seuil ?? 0.7,
  });
  return response.data;
}
