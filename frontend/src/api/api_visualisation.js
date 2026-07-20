import axios from "axios";

// const BASE_URL = "http://localhost:8000";
const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
/** Charge le fichier en RAM backend */
export async function chargerFichier(chemin) {
  const response = await axios.post(`${BASE_URL}/visualisation/charger`, { chemin });
  return response.data;
}

/** Récupère une seule image depuis le cache backend */
export async function getImage(canal, plan_z) {
  const response = await axios.post(`${BASE_URL}/visualisation/image`, { canal, plan_z });
  return response.data;
}
