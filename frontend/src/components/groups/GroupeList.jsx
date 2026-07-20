import { useApp } from "../../context/AppContext";
import styles from "./GroupeList.module.css";

export default function GroupeList({ onSelectFolder }) {
  const { groups, activeGroup, setActiveGroup, activeFile, setActiveFile } = useApp();

  return (
    <div className={styles.container}>
      <p className={styles.label}>Groupes</p>

      {Object.entries(groups).map(([name, group]) => (
        <div key={name} className={styles.group}>
          {/* En-tête du groupe */}
          <div
            className={`${styles.groupHeader} ${activeGroup === name ? styles.active : ""}`}
            onClick={() => setActiveGroup(name)}
          >
            <div className={styles.groupLeft}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
              </svg>
              <span>{name}</span>
            </div>
            <span className={`${styles.badge} ${activeGroup === name ? styles.badgeActive : styles.badgeNeutral}`}>
              {group.files.length}
            </span>
          </div>

          {/* Liste des fichiers si groupe actif */}
          {activeGroup === name && (
            <div className={styles.fileList}>
              {group.files.length === 0 ? (
                <p className={styles.empty}>Aucun fichier chargé</p>
              ) : (
                group.files.map((file) => (
                  <div
                    key={file}
                    className={`${styles.fileItem} ${activeFile === file ? styles.fileActive : ""}`}
                    onClick={() => setActiveFile(file)}
                  >
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M13 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9z" />
                      <polyline points="13 2 13 9 20 9" />
                    </svg>
                    <span>{file}</span>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      ))}

      {/* Bouton charger dossier */}
      <button
        className={styles.loadBtn}
        onClick={() => onSelectFolder(activeGroup)}
      >
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
          <line x1="12" y1="11" x2="12" y2="17" />
          <line x1="9" y1="14" x2="15" y2="14" />
        </svg>
        Charger dossier {activeGroup}
      </button>
    </div>
  );
}
