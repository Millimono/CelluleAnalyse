import { useApp } from "../../context/AppContext";
import styles from "./PipelineStatus.module.css";

const STATUS_ICONS = {
  idle:    { symbol: "○", cls: "idle"    },
  running: { symbol: "◌", cls: "running" },
  done:    { symbol: "✓", cls: "done"    },
  error:   { symbol: "✕", cls: "error"   },
};

export default function PipelineStatus() {
  const { PIPELINE_STEPS, pipelineStatus } = useApp();

  return (
    <div className={styles.container}>
      <p className={styles.label}>Pipeline</p>
      <div className={styles.steps}>
        {PIPELINE_STEPS.map((step, i) => {
          const status = pipelineStatus[step.id] ?? "idle";
          const icon   = STATUS_ICONS[status];
          return (
            <div key={step.id} className={`${styles.step} ${styles[icon.cls]}`}>
              <span className={styles.icon}>{icon.symbol}</span>
              <span className={styles.stepLabel}>{step.label}</span>
              {i < PIPELINE_STEPS.length - 1 && (
                <div className={styles.connector} />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
