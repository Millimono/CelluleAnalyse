import { useApp } from "../../context/AppContext";
import styles from "./FileList.module.css";

export default function FileList() {
  const { groups, activeGroup, activeFile, setActiveFile } = useApp();
  const files = groups[activeGroup]?.files ?? [];

  return (
    <div className={styles.container}>
      <p className={styles.title}>Fichiers — {activeGroup}</p>
      <div className={styles.list}>
        {files.length === 0 ? (
          <p className={styles.empty}>Aucun fichier chargé</p>
        ) : (
          files.map((file) => (
            <div
              key={file}
              className={`${styles.item} ${activeFile === file ? styles.active : ""}`}
              onClick={() => setActiveFile(file)}
            >
              <span className={styles.name}>{file}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
