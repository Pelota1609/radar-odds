import pandas as pd
from pathlib import Path

DATA = Path(__file__).parent / "data" / "sample_odds.csv"

def load_sample_data():
    return pd.read_csv(DATA)

def detect_stale_odds(df, threshold_pct=8.0, min_books=3):
    d = df.copy()
    d["odds"] = pd.to_numeric(d["odds"], errors="coerce")
    d["observed_at"] = pd.to_datetime(d["observed_at"], utc=True, errors="coerce")
    d = d.dropna(subset=["odds", "observed_at"])
    d = d[d["odds"] > 1.0]
    keys = ["event_id", "market", "selection"]
    rows = []
    for _, group in d.groupby(keys, dropna=False):
        if group["bookmaker"].nunique() < min_books:
            continue
        for _, row in group.iterrows():
            peers = group[group["bookmaker"] != row["bookmaker"]]
            if peers.empty:
                continue
            consensus = float(peers["odds"].median())
            diff = (float(row["odds"]) / consensus - 1.0) * 100.0
            if abs(diff) >= threshold_pct:
                peer_time = peers["observed_at"].max()
                gap = (peer_time - row["observed_at"]).total_seconds()
                rows.append({
                    "deporte": row["sport"], "evento": row["event_name"],
                    "mercado": row["market"], "seleccion": row["selection"],
                    "casa": row["bookmaker"], "cuota": float(row["odds"]),
                    "mediana_otras_casas": consensus,
                    "diferencia_pct": diff,
                    "diferencia_timestamps_seg": int(gap),
                    "observado_en": row["observed_at"].isoformat(),
                    "estado": "REVISAR: anomalía no confirmada"
                })
    cols = ["deporte","evento","mercado","seleccion","casa","cuota",
            "mediana_otras_casas","diferencia_pct","diferencia_timestamps_seg",
            "observado_en","estado"]
    if not rows:
        return pd.DataFrame(columns=cols)
    return pd.DataFrame(rows, columns=cols).sort_values(
        "diferencia_pct", key=lambda s: s.abs(), ascending=False)
