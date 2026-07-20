import { useApp } from "../../context/AppContext";
import MetricCard from "./MetricCard";
import styles from "./MetricsGrid.module.css";

export default function MetricsGrid() {
  const { metrics, groups, activeGroup } = useApp();
  const totalFiles = groups[activeGroup]?.files.length ?? 0;

  return (
    <div className={styles.grid}>
      <MetricCard label="Cellules totales"  value={metrics.totalCells}    />
      <MetricCard label="En mitose"         value={metrics.mitosis}        />
      <MetricCard label="% mitose"          value={metrics.mitosisPct} unit="%" />
      <MetricCard label="Fichiers analysés" value={metrics.filesAnalyzed !== null ? `${metrics.filesAnalyzed}/${totalFiles}` : null} />
    </div>
  );
}
