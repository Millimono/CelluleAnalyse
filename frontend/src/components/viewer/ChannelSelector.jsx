import { useApp } from "../../context/AppContext";
import styles from "./ChannelSelector.module.css";

const CHANNELS = [
  { id: "adn",              label: "ADN",               color: "#4488ff" },
  { id: "acetylation",      label: "Acétylation",       color: "#44ff44" },
  { id: "polyglutamylation",label: "PolyGlutamylation", color: "#ff44ff" },
  { id: "adn_acetylation",  label: "ADN + Acétylation", color: "#44aaff" },
  { id: "composite",        label: "Composite",         color: "#ffffff" },
];

export default function ChannelSelector() {
  const { activeChannel, setActiveChannel } = useApp();

  return (
    <div className={styles.selector}>
      {CHANNELS.map((ch) => (
        <button
          key={ch.id}
          className={`${styles.btn} ${activeChannel === ch.id ? styles.active : ""}`}
          onClick={() => setActiveChannel(ch.id)}
          style={activeChannel === ch.id ? { borderColor: ch.color, color: ch.color } : {}}
        >
          <span className={styles.dot} style={{ background: ch.color }} />
          {ch.label}
        </button>
      ))}
    </div>
  );
}