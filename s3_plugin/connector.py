from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
import os
import re

app = Flask(__name__)
app.secret_key = 'some_secret_key'

class S3Connector:
    def __init__(self, aws_access_key, aws_secret_key):
        self.client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
        )

    def fetch_data(self, bucket_name, key):
        data = self.client.get_object(Bucket=bucket_name, Key=key)['Body'].read()

        folder_path = os.path.join(os.getcwd(), 'downloaded_files')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        filename = os.path.basename(key)
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'wb') as file:
            file.write(data)

        email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}")
        emails = email_pattern.findall(data.decode('utf-8'))

        crawled_file_path = os.path.join(folder_path, f"crawled_{filename}.txt")
        with open(crawled_file_path, 'w') as file:
            for email in emails:
                file.write(f"{email}\n")

        return file_path, crawled_file_path

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        aws_access_key = request.form.get('aws_access_key')
        aws_secret_key = request.form.get('aws_secret_key')
        s3_location = request.form.get('s3_location')

        bucket_name, key = s3_location.split("/", 1)
        s3_connector = S3Connector(aws_access_key=aws_access_key, aws_secret_key=aws_secret_key)
        file_path, crawled_file_path = s3_connector.fetch_data(bucket_name, key)

        if file_path and crawled_file_path:
            flash(f"Data fetched from {s3_location} successfully and saved to {file_path}. Crawled data saved to {crawled_file_path}!", "success")
            return redirect(url_for('index'))
        else:
            flash("Failed to fetch data. Please try again.", "danger")
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
