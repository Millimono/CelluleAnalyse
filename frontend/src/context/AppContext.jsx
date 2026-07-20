import { createContext, useContext, useState } from "react";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  // ── Thème ────────────────────────────────────────────────
  const [theme, setTheme] = useState("light");

  const toggleTheme = () => {
    const next = theme === "light" ? "dark" : "light";
    setTheme(next);
    document.documentElement.setAttribute("data-theme", next);
  };

  // ── Groupes ──────────────────────────────────────────────
  const [groups, setGroups] = useState({
    WT: { path: "", files: [] },
    KO: { path: "", files: [] },
  });

  const [activeGroup, setActiveGroup] = useState("WT");
  const [activeFile, setActiveFile]   = useState(null);

  // ── Visualiseur ──────────────────────────────────────────
  const [activeChannel, setActiveChannel] = useState("composite");
  const [activeZ, setActiveZ]             = useState(1);
  const [totalZ, setTotalZ]               = useState(14);

  // ── Pipeline ─────────────────────────────────────────────
  const PIPELINE_STEPS = [
    { id: "chargement",   label: "Chargement"        },
    { id: "projection",   label: "Projection Z"      },
    { id: "noyaux",       label: "Détection noyaux"  },
    { id: "classification", label: "Classification"  },
    { id: "fuseau",       label: "Détection fuseau"  },
    { id: "intensite",    label: "Intensité"         },
    { id: "rapport",      label: "Rapport final"     },
  ];

  const [pipelineStatus, setPipelineStatus] = useState(
    Object.fromEntries(PIPELINE_STEPS.map((s) => [s.id, "idle"]))
    // statuts possibles : "idle" | "running" | "done" | "error"
  );

  // ── Méthodes d'analyse ───────────────────────────────────
  const [methods, setMethods] = useState({
    detection: "threshold",   // threshold | cellpose | stardist
    classification: "shape",  // shape | ml | dl
  });

  // ── Métriques ────────────────────────────────────────────
  const [metrics, setMetrics] = useState({
    totalCells: null,
    mitosis: null,
    mitosisPct: null,
    filesAnalyzed: null,
  });

  return (
    <AppContext.Provider value={{
      // Thème
      theme, toggleTheme,
      // Groupes
      groups, setGroups,
      activeGroup, setActiveGroup,
      activeFile, setActiveFile,
      // Visualiseur
      activeChannel, setActiveChannel,
      activeZ, setActiveZ,
      totalZ, setTotalZ,
      // Pipeline
      PIPELINE_STEPS, pipelineStatus, setPipelineStatus,
      // Méthodes
      methods, setMethods,
      // Métriques
      metrics, setMetrics,
    }}>
      {children}
    </AppContext.Provider>
  );
}

// Hook pour utiliser le contexte facilement
export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp doit être utilisé dans AppProvider");
  return ctx;
}
