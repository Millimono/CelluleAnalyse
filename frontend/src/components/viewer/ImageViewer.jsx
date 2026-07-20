import { useState, useEffect, useRef, useCallback } from "react";
import { useApp } from "../../context/AppContext";
import { chargerFichier, getImage } from "../../api/api_visualisation";
import ChannelSelector from "./ChannelSelector";
import ZSlider from "./ZSlider";
import styles from "./ImageViewer.module.css";

const CANAUX = ["composite", "adn", "acetylation", "polyglutamylation"];

export default function ImageViewer({ imageAnalyse }) {
  const { activeFile, activeChannel, activeZ, setActiveZ, setTotalZ, groups, activeGroup } = useApp();

  const [chargement,  setChargement]  = useState(false);
  const [progression, setProgression] = useState(0);
  const [error,       setError]       = useState(null);
  const [modeAnalyse, setModeAnalyse] = useState(false);

  const imageCache  = useRef({});
  const totalImages = useRef(0);
  const cachedCount = useRef(0);
  const stopPreload = useRef(false);

  const fichierInfo = groups[activeGroup]?.fichiers?.find(f => f.nom === activeFile);
  const cleActive   = `${activeChannel}_z${activeZ}`;
  const imageB64    = modeAnalyse && imageAnalyse
    ? imageAnalyse
    : imageCache.current[cleActive] ?? null;

  // Quand une image analysée arrive → switcher en mode analyse
  useEffect(() => {
    if (imageAnalyse) setModeAnalyse(true);
  }, [imageAnalyse]);

  const fetchEtCacher = useCallback(async (canal, z) => {
    const cle = `${canal}_z${z}`;
    if (imageCache.current[cle] || stopPreload.current) return;
    try {
      const data = await getImage(canal, z);
      imageCache.current[cle] = data.image_b64;
      cachedCount.current += 1;
      setProgression(Math.round((cachedCount.current / totalImages.current) * 100));
    } catch (_) {}
  }, []);

  const genererOrdre = useCallback((zActif, totalZ) => {
    const ordre = [{ canal: "composite", z: zActif }];
    for (const canal of CANAUX) {
      if (canal !== "composite") ordre.push({ canal, z: zActif });
    }
    for (let dist = 1; dist <= totalZ; dist++) {
      for (const z of [zActif + dist, zActif - dist]) {
        if (z < 1 || z > totalZ) continue;
        for (const canal of CANAUX) ordre.push({ canal, z });
      }
    }
    return ordre;
  }, []);

  useEffect(() => {
    if (!fichierInfo) return;
    const charger = async () => {
      stopPreload.current = true;
      imageCache.current  = {};
      cachedCount.current = 0;
      setChargement(true);
      setProgression(0);
      setError(null);
      setModeAnalyse(false);

      try {
        const data = await chargerFichier(fichierInfo.chemin);
        totalImages.current = data.total_z * CANAUX.length;
        stopPreload.current = false;

        await fetchEtCacher("composite", 1);
        setTotalZ(data.total_z);
        setActiveZ(1);
        setChargement(false);

        const ordre = genererOrdre(1, data.total_z);
        for (const { canal, z } of ordre) {
          if (stopPreload.current) break;
          await fetchEtCacher(canal, z);
          await new Promise(r => setTimeout(r, 10));
        }
      } catch (err) {
        setError(err.response?.data?.detail ?? "Erreur chargement");
        setChargement(false);
      }
    };
    charger();
    return () => { stopPreload.current = true; };
  }, [fichierInfo?.chemin]);

  useEffect(() => {
    if (!fichierInfo || chargement) return;
    if (imageCache.current[cleActive]) return;
    fetchEtCacher(activeChannel, activeZ);
  }, [cleActive, chargement]);

  const ouvrirPleinEcran = () => {
    if (!imageB64) return;
    const win = window.open();
    win.document.write(`
      <html>
        <head>
          <title>${activeFile} — Z${activeZ} — ${activeChannel}</title>
          <style>body{margin:0;background:#000;display:flex;align-items:center;justify-content:center;min-height:100vh;}img{max-width:100%;max-height:100vh;object-fit:contain;}</style>
        </head>
        <body><img src="data:image/png;base64,${imageB64}" /></body>
      </html>
    `);
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <p className={styles.title}>{activeFile ?? "Visualiseur d'images"}</p>
        <div className={styles.headerRight}>
          {/* Toggle mode analyse / normal */}
          {imageAnalyse && (
            <button
              className={`${styles.modeBtn} ${modeAnalyse ? styles.modeBtnActive : ""}`}
              onClick={() => setModeAnalyse(!modeAnalyse)}
            >
              {modeAnalyse ? "🔬 Analyse" : "📷 Normal"}
            </button>
          )}
          <ChannelSelector />
          {imageB64 && (
            <button className={styles.fullscreenBtn} onClick={ouvrirPleinEcran}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/>
                <line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/>
              </svg>
              Plein écran
            </button>
          )}
        </div>
      </div>

      <div className={styles.canvas}>
        {chargement && (
          <div className={styles.overlay}>
            <div className={styles.spinner} />
            <p>Chargement du fichier...</p>
          </div>
        )}
        {error && <div className={styles.error}>{error}</div>}
        {imageB64 && !error ? (
          <img src={`data:image/png;base64,${imageB64}`} alt="Image" className={styles.image} />
        ) : !chargement && !error && (
          <div className={styles.empty}>
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
              <rect x="3" y="3" width="18" height="18" rx="2"/>
              <circle cx="8.5" cy="8.5" r="1.5"/>
              <polyline points="21 15 16 10 5 21"/>
            </svg>
            <p>Sélectionne un fichier pour visualiser</p>
          </div>
        )}
      </div>

      {progression > 0 && progression < 100 && (
        <div className={styles.preloadBar}>
          <div className={styles.preloadFill} style={{ width: `${progression}%` }} />
          <span className={styles.preloadLabel}>Cache {progression}%</span>
        </div>
      )}
      {progression === 100 && (
        <div className={styles.preloadDone}>✓ Cache complet — navigation instantanée</div>
      )}

      <ZSlider />
    </div>
  );
}
