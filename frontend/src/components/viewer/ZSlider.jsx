import { useApp } from "../../context/AppContext";
import styles from "./ZSlider.module.css";

export default function ZSlider() {
  const { activeZ, setActiveZ, totalZ } = useApp();

  const prev = () => setActiveZ((z) => Math.max(1, z - 1));
  const next = () => setActiveZ((z) => Math.min(totalZ, z + 1));

  return (
    <div className={styles.container}>
      <span className={styles.label}>Plan Z</span>

      <div className={styles.btnGroup}>
        <button className={styles.btn} onClick={prev} title="Plan précédent">‹</button>
        <button className={styles.btn} onClick={next} title="Plan suivant">›</button>
      </div>

      <input
        type="range"
        min={1}
        max={totalZ}
        value={activeZ}
        step={1}
        className={styles.slider}
        onChange={(e) => setActiveZ(Number(e.target.value))}
      />

      <span className={styles.value}>{activeZ} / {totalZ}</span>
    </div>
  );
}
