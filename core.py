import pandas as pd

def verileri_eslestir(irsaliye_excel_path, fatura_excel_path):
    # Excel dosyalarını okuma
    df_irsaliye = pd.read_excel(irsaliye_excel_path)
    df_fatura = pd.read_excel(fatura_excel_path)
    
    # Bellek optimizasyonu (Veri tiplerini küçültme)
    df_irsaliye['irsaliye_no'] = df_irsaliye['irsaliye_no'].astype(str)
    df_fatura['irsaliye_no'] = df_fatura['irsaliye_no'].astype(str)
    
    df_irsaliye['tutar'] = pd.to_numeric(df_irsaliye['tutar'], downcast='float')
    df_fatura['tutar'] = pd.to_numeric(df_fatura['tutar'], downcast='float')
    df_fatura['kdv_orani'] = pd.to_numeric(df_fatura['kdv_orani'], downcast='float')

    # Dataframe'leri irsaliye_no üzerinden OUTER JOIN ile birleştirme
    df_merged = pd.merge(
        df_irsaliye, 
        df_fatura, 
        on='irsaliye_no', 
        how='outer', 
        suffixes=('_irsaliye', '_fatura')
    )
    
    # Uyuşmazlık Durumlarını Kontrol Etme
    # 1. Tutar farkı
    df_merged['tutar_farki'] = (df_merged['tutar_irsaliye'] - df_merged['tutar_fatura']).abs()
    
    # 2. Durum Tespiti
    def durum_belirle(row):
        if pd.isna(row['tutar_irsaliye']):
            return "Eksik İrsaliye Kaydı"
        elif pd.isna(row['tutar_fatura']):
            return "Eksik Fatura Kaydı"
        elif row['tutar_farki'] > 0.01:  # Küçük yuvarlama hataları tolere edilebilir
            return "Tutar Uyuşmazlığı"
        elif row['kdv_orani'] not in [0.0, 0.01, 0.10, 0.20]:  # Örnek KDV kontrolü
            return "Hatalı KDV Oranı"
        else:
            return "Eşleşti"

    df_merged['Durum'] = df_merged.apply(durum_belirle, axis=1)
    return df_merged
