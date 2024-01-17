import boto3

def test_s3_connection():
    try:
        # 创建 S3 客户端
        s3 = boto3.client('s3')

        # 尝试列出 S3 存储桶
        buckets = s3.list_buckets()

        # 如果成功列出存储桶，则连接正常
        print("AWS S3 连接正常，可访问的存储桶列表：")
        for bucket in buckets['Buckets']:
            print(bucket['Name'])

    except Exception as e:
        # 打印详细的错误信息
        print("AWS S3 连接失败，错误信息：", str(e))

if __name__ == "__main__":
    test_s3_connection()