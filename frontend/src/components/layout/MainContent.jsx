import { useState } from "react";
import MetricsGrid from "../metrics/MetricsGrid";
import ImageViewer from "../viewer/ImageViewer";
import FileList from "../files/FileList";
import MethodSelector from "../analysis/MethodSelector";
import styles from "./MainContent.module.css";

export default function MainContent() {
  const [imageAnalyse, setImageAnalyse] = useState(null);

  const handleResultat = (resultat) => {
    setImageAnalyse(resultat.image_b64);
  };

  return (
    <main className={styles.main}>
      <MetricsGrid />
      <ImageViewer imageAnalyse={imageAnalyse} />
      <div className={styles.bottom}>
        <FileList />
        <MethodSelector onResultat={handleResultat} />
      </div>
    </main>
  );
}
