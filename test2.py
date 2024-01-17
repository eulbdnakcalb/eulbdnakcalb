import boto3

def test_s3_connection():
    try:
        # S3クライアントを作成
        s3 = boto3.client('s3')

        # S3バケットをリストアップしてみる
        buckets = s3.list_buckets()

        # バケットのリストが取得できれば、接続は正常
        print("AWS S3接続は正常で、アクセス可能なバケットのリスト：")
        for bucket in buckets['Buckets']:
            print(bucket['Name'])

    except Exception as e:
        # 詳細なエラーメッセージを出力
        print("AWS S3接続に失敗しました。エラーメッセージ：", str(e))

if __name__ == "__main__":
    test_s3_connection()
