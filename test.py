import pandas as pd
import os

def load_contact_list(file_path):
    """連絡先一覧.xlsxから削除ユーザーを読み込む"""
    sheets = ['システム主管連絡先', 'AP運用連絡先', 'AP保守連絡先', 'インフラ運用保守']
    all_deleted = []
    
    for sheet in sheets:
        df = pd.read_excel(file_path, sheet_name=sheet, header=2)
        
        if '削除フラグ' in df.columns:
            deleted = df[df['削除フラグ'] == 1].copy()
            deleted['シート名'] = sheet
            all_deleted.append(deleted)
    
    return pd.concat(all_deleted, ignore_index=True) if all_deleted else pd.DataFrame()

def check_user_existence(deleted_users, ledger_path):
    """削除ユーザーが台帳に存在するか確認"""
    ledger_df = pd.read_excel(ledger_path, sheet_name='ユーザ採番台帳', header=1)
    results = []
    
    for _, user in deleted_users.iterrows():
        email = user['メール']
        sheet = user['シート名']
        exists = False
        
        if sheet in ['システム主管連絡先', 'AP運用連絡先', 'AP保守連絡先']:
            # メールはF列(インデックス5)
            # 払出状況はZ列(インデックス26)
            for _, row in ledger_df.iterrows():
                if len(row) > 5 and pd.notna(row.iloc[5]) and str(row.iloc[5]).strip() == str(email).strip():
                    if len(row) > 26 and pd.notna(row.iloc[26]) and str(row.iloc[26]).strip() == '●':
                        exists = True
                        break
        
        elif sheet == 'インフラ運用保守':
            # メールはDC列(インデックス106)
            # 払出状況はDX列(インデックス127)
            for _, row in ledger_df.iterrows():
                if len(row) > 106 and pd.notna(row.iloc[106]) and str(row.iloc[106]).strip() == str(email).strip():
                    if len(row) > 127 and pd.notna(row.iloc[127]) and str(row.iloc[127]).strip() == '●':
                        exists = True
                        break
            
            # メールはFA列(インデックス156)
            # 払出状況はFV列(インデックス177)
            if not exists:
                for _, row in ledger_df.iterrows():
                    if len(row) > 156 and pd.notna(row.iloc[156]) and str(row.iloc[156]).strip() == str(email).strip():
                        if len(row) > 177 and pd.notna(row.iloc[177]) and str(row.iloc[177]).strip() == '●':
                            exists = True
                            break
        
        results.append({
            'シート名': sheet,
            '氏名': user['氏名'],
            'メール': email,
            '状態': '存在する' if exists else '存在しない'
        })
    
    return results

def main():
    contact_path = r"C:\Users\yh980\work\棚卸スクリプト\連絡先一覧.xlsx"
    ledger_path = r"C:\Users\yh980\work\棚卸スクリプト\台帳.xlsx"
    
    print("削除ユーザー存在チェックスクリプトを開始します...")
    print("-" * 60)
    
    # ファイル存在確認
    if not os.path.exists(contact_path):
        print(f"エラー: ファイルが見つかりません - {contact_path}")
        return
    if not os.path.exists(ledger_path):
        print(f"エラー: ファイルが見つかりません - {ledger_path}")
        return
    
    try:
        # 1. 連絡先一覧から削除ユーザーを抽出
        deleted_users = load_contact_list(contact_path)
        
        if deleted_users.empty:
            print("削除フラグが立っているユーザーはありません。")
            return
        
        # 2. チェック実行
        results = check_user_existence(deleted_users, ledger_path)
        
        # 3. 結果表示
        print("\nチェック結果")
        print("="*40)
        
        existing = [r for r in results if r['状態'] == '存在する']
        non_existing = [r for r in results if r['状態'] == '存在しない']
        
        if existing:
            print("× 以下の削除済みユーザーが台帳にまだ存在しています：")
            for r in existing:
                print(f"  - {r['シート名']}: {r['氏名']} ({r['メール']})")
        
        if non_existing:
            print(f"\n✓ 以下の削除済みユーザーは台帳に存在しません：")
            for r in non_existing:
                print(f"  - {r['シート名']}: {r['氏名']}")
        
        # 4. Excel出力
        output_path = r"C:\Users\yh980\work\棚卸スクリプト\削除ユーザー存在チェック結果.xlsx"
        pd.DataFrame(results).to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"\n詳細結果をExcelファイルに出力しました: {output_path}")
        print(f"\n総チェック数: {len(results)}件")
        print(f"存在が確認された件数: {len(existing)}件")
        print(f"存在しない件数: {len(non_existing)}件")
        
    except Exception as e:
        print(f"エラー: {str(e)}")

if __name__ == "__main__":
    main()
    print("\n処理が完了しました。")