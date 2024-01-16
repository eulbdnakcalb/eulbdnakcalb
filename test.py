import os
import json
import boto3
from datetime import datetime, timedelta

def file_read(file_path):
    """
    設定ファイルから変数を読み取ります。

    パラメータ：
    - file_path (str): 設定ファイルのパス。

    戻り値：
    - config (dict): 設定ファイルの変数。
    """
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config

def yesterday(date_format="%Y%m%d"):
    """
    前日の日付を取得します。

    パラメータ：
    - date_format (str): 日付のフォーマット。

    戻り値：
    - str: 前日の日付。
    """
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime(date_format)

def StorageClass_change(config):
    """
    指定されたS3バケットおよびプレフィックスのすべてのオブジェクトを複製します。

    パラメータ：
    - config (dict): 設定ファイルの変数。

    戻り値：
    - None
    """
    # 設定ファイルから変数を取得
    bucket_name = config.get('bucket_name')
    folder_prefixes = config.get('folder_prefixes', [])
    base_folder = config.get('base_folder', "")
    date_format = config.get('date_format', "%Y%m%d")
    new_storage_class = config.get('new_storage_class')
    access_key_id = config.get('access_key_id')
    secret_access_key = config.get('secret_access_key')

    # S3クライアントを作成し、提供された資格情報を使用する
    s3 = boto3.client('s3',
                     aws_access_key_id=access_key_id,
                     aws_secret_access_key=secret_access_key)

    for folder_prefix in folder_prefixes:
        # フォルダのパスを構築
        folder_path = f"{base_folder}/{folder_prefix}/{yesterday(date_format)}"

        # 指定されたプレフィックスのすべてのオブジェクトをリストアップ
        response = s3.list_objects(Bucket=bucket_name, Prefix=folder_path)
        objects = response.get('Contents', [])  # 'Contents' フィールドが存在しない場合は空のリストを返す

        # 各オブジェクトのストレージクラス変更
        for obj in objects:
            key = obj['Key']
            print(f"オブジェクトのストレージクラス変更中：{key}")

            # ストレージクラス変更
            s3.copy_object(
                Bucket=bucket_name,
                CopySource={'Bucket': bucket_name, 'Key': key},
                Key=key,
                StorageClass=new_storage_class
            )

    print("ストレージクラスの変更が完了しました。")

if __name__ == "__main__":
    # 設定ファイルのパス
    conf_file_path = os.path.join('D:\\python', 'test.conf')

    # 設定ファイルを読み取る
    config = file_read(conf_file_path)

    # オブジェクトを複製するための関数を呼び出す
    StorageClass_change(config)





