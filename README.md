# discord_bot

### 設定
#### config.py
Discordボットのコマンド
* api_token: DiscordボットのAPIトークン。開発者ポータルのアプリケーション→Botの設定情報から取得。トークンは1度しか表示されないので、忘れたらリセットして取得し直す。
* srv_list: EC2の管理するサーバーリスト。1つのエントリーは辞書型で記述
  - name: サーバー名。Discordでのコマンドで指定するキーになるのでユニークに
  - type: ec2 のみ
  - instance_id: EC2のインスタンスID。AWSポータルから管理するEC2のインスタンスIDを取得して設定

#### aws/ec2/config.py
AWSのAPIアクセスに必要な情報。AWSポータルのアカウント→セキュリティ認証情報→アクセスキーで作成して設定
* AWS_ACCESS_KEY_ID: IAM ユーザーまたはロールに関連付けられている AWS アクセスキー
* AWS_SECRET_KEY: IDに紐づく鍵。作成時にのみ表示されるので、忘れたら新規作成する


#### サービス起動設定
* /opt/discord_bot にソースを展開。↑2件をそれぞれファイルに設定
* service/discord_bot.service を`/etc/systemd/system/`に配置
* サービス登録 `sudo systemctl enable discord_bot`
* サービス起動 `sudo systemctl start discord_bot`
* ステータス確認 `systemctl status discord_bot`
