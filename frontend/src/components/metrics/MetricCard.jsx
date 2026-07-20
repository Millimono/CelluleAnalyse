import styles from "./MetricCard.module.css";

export default function MetricCard({ label, value, unit = "" }) {
  return (
    <div className={styles.card}>
      <p className={styles.label}>{label}</p>
      <p className={styles.value}>
        {value !== null && value !== undefined ? `${value}${unit}` : "—"}
      </p>
    </div>
  );
}
