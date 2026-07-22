import styles from "./MetricsGrid.module.css";

export default function MetricsGrid() {
  return (
    <div className={styles.instructions}>
      <p className={styles.step}>
        <span className={styles.num}>1</span>
        Chargez vos dossiers <strong>WT</strong> et <strong>KO</strong> depuis la sidebar
      </p>
      <p className={styles.step}>
        <span className={styles.num}>2</span>
        Sélectionnez un fichier pour le visualiser
      </p>
      <p className={styles.step}>
        <span className={styles.num}>3</span>
        Configurez et lancez l'analyse
      </p>
      <p className={styles.step}>
        <span className={styles.num}>4</span>
        Consultez les résultats ci-dessous
      </p>
    </div>
  );
}