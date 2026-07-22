import { useState } from "react";
import { useApp } from "../../context/AppContext";
import { detecterNoyaux } from "../../api/api_analyse";
import styles from "./MethodSelector.module.css";

const DETECTION_METHODS = [
  { id: "threshold", label: "Seuillage (Otsu)" },
  { id: "cellpose",  label: "Cellpose (ML)"    },
  { id: "stardist",  label: "StarDist (DL)"    },
];

const CLASSIFICATION_METHODS = [
  { id: "shape", label: "Forme géométrique" },
  { id: "ml",    label: "ML classique"      },
  { id: "dl",    label: "Deep Learning"     },
];

const ANALYSES = [
  { id: "comptage",  label: "Comptage des cellules",  desc: "Noyaux + interphase vs mitose",          available: true  },
  { id: "intensite", label: "Mesure d'intensité",     desc: "Fluorescence tubuline dans les fuseaux", available: true  },
  { id: "morpho",    label: "Morphologie fuseau",     desc: "Forme, taille, orientation",             available: false },
];

export default function MethodSelector({ onResultat }) {
  const { methods, setMethods, activeFile, activeGroup, groups, setMetrics, setPipelineStatus } = useApp();

  const [scope,            setScope]            = useState("fichier");
  const [selectedGroups,   setSelectedGroups]   = useState({ WT: false, KO: false });
  const [selectedAnalyses, setSelectedAnalyses] = useState({ comptage: true, intensite: false, morpho: false });
  const [loading,          setLoading]          = useState(false);
  const [error,            setError]            = useState(null);

  const toggleGroupe  = (name) => setSelectedGroups((p) => ({ ...p, [name]: !p[name] }));
  const toggleAnalyse = (id)   => setSelectedAnalyses((p) => ({ ...p, [id]: !p[id] }));
  const updateMethod  = (k, v) => setMethods((p) => ({ ...p, [k]: v }));

  const handleLancer = async () => {
    if (!activeFile && scope === "fichier") {
      setError("Aucun fichier sélectionné !");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      // ── Comptage des cellules ──────────────────────────
      if (selectedAnalyses.comptage) {
        setPipelineStatus((p) => ({ ...p, noyaux: "running" }));

        const resultat = await detecterNoyaux({
          methode:    methods.detection,
          projection: "max",
        });

        // Mettre à jour les métriques
        setMetrics({
          totalCells:    resultat.total,
          mitosis:       resultat.mitose,
          inconnu:       resultat.inconnu,
          mitosisPct:    resultat.total > 0
            ? Math.round((resultat.mitose / resultat.total) * 100)
            : 0,
          filesAnalyzed: 1,
        });

        setPipelineStatus((p) => ({ ...p, noyaux: "done", classification: "done" }));

        // Envoyer l'image annotée au visualiseur
        if (onResultat) onResultat(resultat);
      }

    } catch (err) {
      setError(err.response?.data?.detail ?? "Erreur lors de l'analyse");
      setPipelineStatus((p) => ({ ...p, noyaux: "error" }));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <p className={styles.title}>Configurer l'analyse</p>

      {/* Périmètre */}
      <div className={styles.section}>
        <p className={styles.sectionLabel}>Périmètre</p>
        <div className={styles.scopeList}>
          <label className={`${styles.scopeOption} ${scope === "fichier" ? styles.scopeActive : ""}`}>
            <input type="radio" name="scope" checked={scope === "fichier"} onChange={() => setScope("fichier")} />
            <div>
              <p className={styles.optionTitle}>Fichier en cours</p>
              <p className={styles.optionDesc}>{activeFile ?? "Aucun fichier sélectionné"}</p>
            </div>
          </label>

          <label className={`${styles.scopeOption} ${scope === "groupes" ? styles.scopeActive : ""}`}>
            <input type="radio" name="scope" checked={scope === "groupes"} onChange={() => setScope("groupes")} />
            <div style={{ flex: 1 }}>
              <p className={styles.optionTitle}>Groupes</p>
              <div className={styles.groupeChecks}>
                {Object.keys(groups).map((name) => (
                  <label key={name} className={styles.groupeCheck}>
                    <input type="checkbox" checked={selectedGroups[name] ?? false}
                      onChange={() => toggleGroupe(name)} disabled={scope !== "groupes"} />
                    {name} ({groups[name].files.length})
                  </label>
                ))}
              </div>
            </div>
          </label>
        </div>
      </div>

      {/* Analyses */}
      <div className={styles.section}>
        <p className={styles.sectionLabel}>Analyses</p>
        <div className={styles.analyseList}>
          {ANALYSES.map((a) => (
            <label key={a.id} className={`${styles.analyseOption} ${!a.available ? styles.disabled : ""}`}>
              <input type="checkbox" checked={selectedAnalyses[a.id] ?? false}
                onChange={() => toggleAnalyse(a.id)} disabled={!a.available} />
              <div>
                <p className={styles.optionTitle}>
                  {a.label}
                  {!a.available && <span className={styles.soon}>bientôt</span>}
                </p>
                <p className={styles.optionDesc}>{a.desc}</p>
              </div>
            </label>
          ))}
        </div>
      </div>

      {/* Méthode */}
      <div className={styles.section}>
        <p className={styles.sectionLabel}>Méthode</p>
        <div className={styles.methodGrid}>
          <div>
            <label className={styles.fieldLabel}>Détection noyaux</label>
            <select value={methods.detection} onChange={(e) => updateMethod("detection", e.target.value)}>
              {DETECTION_METHODS.map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}
            </select>
          </div>
          <div>
            <label className={styles.fieldLabel}>Classification</label>
            <select value={methods.classification} onChange={(e) => updateMethod("classification", e.target.value)}>
              {CLASSIFICATION_METHODS.map((m) => <option key={m.id} value={m.id}>{m.label}</option>)}
            </select>
          </div>
        </div>
      </div>

      {error && <div className={styles.error}>{error}</div>}

      <button
        className={`${styles.runBtn} primary`}
        onClick={handleLancer}
        disabled={loading}
      >
        {loading ? "Analyse en cours..." : "Lancer l'analyse"}
      </button>
    </div>
  );
}