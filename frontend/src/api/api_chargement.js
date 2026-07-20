import axios from "axios";

// const BASE_URL = "http://localhost:8000";
const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
/**
 * Scanner un dossier et retourner la liste des fichiers .nd2
 * @param {string} chemin - chemin absolu du dossier
 */
export async function scannerDossier(chemin) {
  const response = await axios.post(`${BASE_URL}/chargement/scanner`, {
    chemin,
  });
  return response.data;
}
