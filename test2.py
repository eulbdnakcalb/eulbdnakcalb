import pandas as pd

def load_config():
    """加载配置文件"""
    config_path = r"C:\Users\yh980\SK\conf\UserCompare.conf"
    config = {}
    with open(config_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    return config

def main():
    print("台帳とADエクスポートのユーザー比較を開始します...")
    print("-" * 60)
    
    try:
        # 加载配置
        config = load_config()
        
        # 从配置文件获取路径
        ledger_path = config['ledger']
        ad_path = config['ad_export']
        output_path = config['ledger_ad_result']
        
        # 1. 台帳から払出状況が●のユーザーを抽出
        ledger_df = pd.read_excel(ledger_path, sheet_name='ユーザ採番台帳', header=1)
        
        ledger_emails = []
        
        # 第一部分: F列(5)メール, AA列(26)払出状況
        for _, row in ledger_df.iterrows():
            if len(row) > 26 and pd.notna(row.iloc[26]) and str(row.iloc[26]).strip() == '●':
                if len(row) > 5 and pd.notna(row.iloc[5]):
                    ledger_emails.append(str(row.iloc[5]).strip().lower())
        
        # 第二部分: DC列(106)メール, DX列(127)払出状況
        for _, row in ledger_df.iterrows():
            if len(row) > 127 and pd.notna(row.iloc[127]) and str(row.iloc[127]).strip() == '●':
                if len(row) > 106 and pd.notna(row.iloc[106]):
                    ledger_emails.append(str(row.iloc[106]).strip().lower())
        
        # 第三部分: FA列(156)メール, FV列(177)払出状況
        for _, row in ledger_df.iterrows():
            if len(row) > 177 and pd.notna(row.iloc[177]) and str(row.iloc[177]).strip() == '●':
                if len(row) > 156 and pd.notna(row.iloc[156]):
                    ledger_emails.append(str(row.iloc[156]).strip().lower())
        
        print(f"台帳から {len(ledger_emails)} 件の払出状況●ユーザーを抽出しました")
        
        # 2. ADエクスポートからユーザーを抽出
        ad_df = pd.read_excel(ad_path, sheet_name='AD_export_user', header=1)
        
        ad_emails = set()
        
        # C列をmailとして使用
        if len(ad_df.columns) > 2:
            mail_col = ad_df.columns[2]
            for _, row in ad_df.iterrows():
                if pd.notna(row[mail_col]):
                    ad_emails.add(str(row[mail_col]).strip().lower())
        
        print(f"ADエクスポートから {len(ad_emails)} 件のユーザーを抽出しました")
        
        # 3. 比較処理
        results = []
        missing_users = []
        
        for email in ledger_emails:
            exists = email in ad_emails
            results.append({
                'メール': email,
                'AD存在': '○' if exists else '×'
            })
            
            if not exists:
                missing_users.append(email)
        
        # 4. 結果表示
        print("\n比較結果")
        print("=" * 40)
        
        existing_count = len(ledger_emails) - len(missing_users)
        
        if missing_users:
            print("× ADに存在しないユーザー:")
            for email in missing_users:
                print(f"  - {email}")
        
        print(f"\n総チェック数: {len(ledger_emails)}件")
        print(f"ADに存在する: {existing_count}件")
        print(f"ADに存在しない: {len(missing_users)}件")
        
        # 結果をExcelに輸出
        pd.DataFrame(results).to_excel(output_path, index=False, engine='openpyxl')
        
        print(f"\n詳細結果をExcelファイルに出力しました: {output_path}")
        
    except Exception as e:
        print(f"エラー: {str(e)}")

if __name__ == "__main__":
    main()
    print("\n処理が完了しました。")