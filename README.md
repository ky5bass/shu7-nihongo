# ワークフロー

ローカルで以下のコマンドを順に実行する。
```zsh
cd $HOME/dev/sh7n-bundle
npm install wrangler --save-dev     # wranglerをdevDependenciesとしてインストール
npx wrangler login                  # Cloudflareログイン
npm create cloudflare@latest        # Workersプロジェクトを作成
# ↑の質問への回答:
#   In which directory do you want to create your application?  -> ./shu7-nihongo
#   What would you like to start with?                          -> Hello World example
#   Which template would you like to use?                       -> Hello World Worker
#   Which language do you want to use?                          -> TypeScript
#   Do you want to use git for version control?                 -> Yes
#   Do you want to deploy your application?                     -> No
cd shu7-nihongo

vi wrangler.toml
# ↓を追記
# # Workers Site
# # 参考 https://developers.cloudflare.com/workers/configuration/sites/start-from-worker/
# [site]
# bucket = "./public"     # the directory with your static assets
npm install @cloudflare/kv-asset-handler --save-dev     # kv-asset-handlerをdevDependenciesとしてインストール
cp -r $SH7N_DEV_CONFIG/public .     # 暫定的にpublicを用意
                                    # (用意しないとデプロイに失敗する。
                                    #  テスト用のものになっているのが望ましい)

SH7N_DEV_CONFIG=$HOME/dev/sh7n-bundle/sh7n-dev4
cp -r $SH7N_DEV_CONFIG/.github \
      $SH7N_DEV_CONFIG/static \
      $SH7N_DEV_CONFIG/templates \
      $SH7N_DEV_CONFIG/Makefile \
      $SH7N_DEV_CONFIG/main.py \
      $SH7N_DEV_CONFIG/requirements.txt .
cp -f $SH7N_DEV_CONFIG/src/index.ts src/index.ts
vi .github/workflows/daily-build-trigger.yml
# ↓のように変更
# -  # # 定期実行
# -  # # 参考 https://qiita.com/cardene/items/67d31f13d27865a12ecf#設定
# -  # # 注 よく遅延するらしいので、気長に待とう
# -  # #    参考 https://zenn.dev/no4_dev/articles/14b295b8dafbfd
# -  # schedule:
# -  #   - cron: '0 21 * * *'  # 日本時間AM6:00
# -  # ↑挙動を確認できたので、dev環境での定期実行はもう不要
# +  # 定期実行
# +  # 参考 https://qiita.com/cardene/items/67d31f13d27865a12ecf#設定
# +  # 注 よく遅延するらしいので、気長に待とう
# +  #    参考 https://zenn.dev/no4_dev/articles/14b295b8dafbfd
# +  schedule:
# +    - cron: '0 21 * * *'  # 日本時間AM6:00
vi .gitignore
# ↓を追記
# # --------------------↓以降、自分で追加↓--------------------
# 
# # アセット
# public/
sed -i '' s/.dev.1//g Makefile      # Makefile内で".dev.1"を除去(""に置換)
# 注 ↑はmacOSにおいてのみ有効(macOSのsedはBSD版であるため)。
#    Linux等のGNU版sedでは `sed -i s/.dev.1//g Makefile` らしい。
#    参考 https://qiita.com/catfist/items/1156ae0c7875f61417ee
vi wrangler.toml
# ↓を上のほうに追記
# # カスタムドメイン
# # 参考 https://developers.cloudflare.com/workers/configuration/routing/custom-domains/
# routes = [
#   { pattern = "shop.example.com", custom_domain = true }
# ]

npx wrangler deploy     # 初めてのデプロイ
                        # (手早くリモート上にプロジェクトを作成するために一度だけ実行。
                        #  以降はこのようなローカルからのデプロイはしない)
```

次に、GitHubに`shu7-nihongo`という名前で**Publicリポジトリ**を作成し、プッシュ。
(詳細な手順は省略)  
また、GitHubダッシュボードで  
**Settings > Actions > General > Workflow permissions を「Read and write permissions」にしておくこと**。

最後に、ダッシュボードから以下の設定を行う。
```yaml
変数とシークレット:
    - タイプ: シークレット
      名前: SH7N_PASSWORD
      値: 値が暗号化されました  # 注 適切な値に変更すること。以降も同様。
    - タイプ: シークレット
      名前: SH7N_USER
      値: 値が暗号化されました

ビルド(ベータ版):
    Git リポジトリ: ky5bass/shu7-nihongo
    ビルド構成:
        ビルド コマンド: make build
        デプロイ コマンド: npx wrangler deploy
        ルート ディレクトリ: /
    ブランチ コントロール:
        プロダクション ブランチ: main
    監視パスを構築する:
        パスを含む: *
    API トークン:
        名前: Workers Builds - 2024-12-10 01:17
    変数とシークレット:
        - タイプ: シークレット
          名前: SUPABASE_KEY
          値: 値が暗号化されました
        - タイプ: シークレット
          名前: SUPABASE_URL
          値: 値が暗号化されました
    ビルド キャッシュ: 無効
```