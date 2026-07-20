import { useState } from "react";
import { useApp } from "../../context/AppContext";
import { scannerDossier } from "../../api/api_chargement";
import GroupeList from "../groups/GroupeList";
import PipelineStatus from "../pipeline/PipelineStatus";
import styles from "./Sidebar.module.css";

export default function Sidebar() {
  const { setGroups, setPipelineStatus } = useApp();
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState(null);

  const handleSelectFolder = async (groupName) => {
    const chemin = prompt(`Chemin du dossier ${groupName} :\nEx: I:\\Stages Bio-info\\MAP6 images\\WT`);
    if (!chemin) return;

    setLoading(true);
    setError(null);

    try {
      const data = await scannerDossier(chemin);

      setGroups((prev) => ({
        ...prev,
        [groupName]: {
          path: data.chemin,
          files: data.fichiers.map((f) => f.nom),
          fichiers: data.fichiers,
        },
      }));

      setPipelineStatus((prev) => ({ ...prev, chargement: "done" }));

    } catch (err) {
      const msg = err.response?.data?.detail ?? "Erreur de connexion au serveur";
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <aside className={styles.sidebar}>
      {error   && <div className={styles.error}>{error}</div>}
      {loading && <div className={styles.loading}>Chargement...</div>}
      <GroupeList onSelectFolder={handleSelectFolder} />
      <PipelineStatus />
    </aside>
  );
}
