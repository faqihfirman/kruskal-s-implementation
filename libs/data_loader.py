import pandas as pd
import os

class DataLoader:
    
    COL_ASAL = 'Asal'
    COL_TUJUAN = 'Tujuan'
    COL_JARAK = 'Jarak (Km)'
    COL_BIAYA = 'Biaya (Juta Rp)'
    COL_BENEFIT = 'Benefit (Skor 1-100)'

    @staticmethod
    def load_road_data(csv_path):
  
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"File database tidak ditemukan: {csv_path}")

        try:
            df = pd.read_csv(csv_path)
        except Exception as e:
            raise ValueError(f"Gagal membaca file CSV. Pastikan format benar. Error: {e}")

        required_cols = [
            DataLoader.COL_ASAL, DataLoader.COL_TUJUAN, 
            DataLoader.COL_JARAK, DataLoader.COL_BIAYA, DataLoader.COL_BENEFIT
        ]

        if not set(required_cols).issubset(df.columns):
            raise ValueError(f"Format CSV Salah! Kolom wajib: {required_cols}")


        unique_villages = pd.concat([df[DataLoader.COL_ASAL], df[DataLoader.COL_TUJUAN]]).unique()
        village_names = sorted(unique_villages.tolist())
        village_map = {name: i for i, name in enumerate(village_names)}

        road_data = []
        for _, row in df.iterrows():
            try:
                u_idx = village_map[row[DataLoader.COL_ASAL]]
                v_idx = village_map[row[DataLoader.COL_TUJUAN]]
                
                road_data.append({
                    'u': u_idx,
                    'v': v_idx,
                    'distance': float(row[DataLoader.COL_JARAK]),
                    'cost': float(row[DataLoader.COL_BIAYA]),
                    'benefit': float(row[DataLoader.COL_BENEFIT])
                })
            except KeyError as e:
                print(f"[Warning] Desa {e} tidak terdaftar di mapping. Baris dilewati.")
                
        print(f"DataLoader: Berhasil memuat {len(village_names)} desa dan {len(road_data)} rute jalan.")
        
        return village_names, road_data