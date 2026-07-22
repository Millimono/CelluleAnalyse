import styles from "./ResultatsAnalyse.module.css";

export default function ResultatsAnalyse({ resultats }) {
  if (!resultats) return null;

  const { total, interphase, mitose, inconnu, mesures_fuseau } = resultats;

  return (
    <div className={styles.container}>
      <p className={styles.title}>Résultats de l'analyse</p>

      {/* Résumé */}
     {/* Résumé */}
      <div className={styles.summary}>
        <div className={styles.stat}>
          <span className={styles.statLabel}>Total</span>
          <span className={styles.statValue}>{total}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statLabel}>Interphase</span>
          <span className={`${styles.statValue} ${styles.green}`}>{interphase}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statLabel}>Mitose</span>
          <span className={`${styles.statValue} ${styles.red}`}>{mitose}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statLabel}>Inconnu</span>
          <span className={`${styles.statValue} ${styles.yellow}`}>{inconnu}</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statLabel}>% Mitose</span>
          <span className={styles.statValue}>
            {total > 0 ? Math.round((mitose / total) * 100) : 0}%
          </span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statLabel}>Fichiers analysés</span>
          <span className={styles.statValue}>{resultats.fichiers_analyses ?? 1}</span>
        </div>
      </div>

      {/* Intensités des fuseaux mitotiques */}
      {mesures_fuseau && mesures_fuseau.length > 0 && (
        <div className={styles.fuseaux}>
          <p className={styles.subtitle}>Intensité des fuseaux mitotiques</p>
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Cellule</th>
                <th>Acétylation (moy)</th>
                <th>PolyGlu (moy)</th>
                <th>Acétylation (max)</th>
                <th>PolyGlu (max)</th>
                <th>Ratio PolyGlu/Acét</th>
              </tr>
            </thead>
            <tbody>
              {mesures_fuseau.map((m) => (
                <tr key={m.noyau_id}>
                  <td>#{m.noyau_id}</td>
                  <td className={styles.green}>{m.intensite_acetylation}</td>
                  <td className={styles.magenta}>{m.intensite_polyglutamylation}</td>
                  <td className={styles.green}>{m.intensite_max_acetylation}</td>
                  <td className={styles.magenta}>{m.intensite_max_polyglutamylation}</td>
                  <td>{m.ratio_poly_acet}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {mesures_fuseau && mesures_fuseau.length === 0 && (
        <p className={styles.empty}>Aucune mitose détectée — pas de mesure d'intensité</p>
      )}
    </div>
  );
}
