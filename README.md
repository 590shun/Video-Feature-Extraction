# Video-Feature-Extraction
このリポジトリは動画の特徴抽出器のコードをまとめたものです。  
ベースとなっている手法は[こちら](https://arxiv.org/abs/1705.07750)で、自分で使うために書き直しました。  
実行のための手順を記してあります。  

# 編集が必要なコードについて  
## preprocess.sh
前提として動画からフレームの切り出しをするのに[ffmpeg](https://ffmpeg.org/)を使用します。  
こちらは参考になる[記事(例)](https://qiita.com/cha84rakanal/items/e84fe4eb6fbe2ae13fd8)があるので参考にしてください。  
1.settings  
(1)CONVERT_VIDEO_TO_IMG: true or false  
(2)CROP_VIDEO: true or false  
(3)RUN_I3D_PYTORCH: true(固定)

2.video information
(1)frame_rate: 動画のframe rateに合わせる  
(2)dir_image: 切り出した画像の出力先  
(3)name_image: 切り出した画像に通し番号を付与  
(4)extension_image: 切り出した画像の拡張子を指定  

3.optional information  
(1)start_time_sec: 切り出しの開始位置  
(2)continuous_time_sec: 切り出しの時間範囲(大きめの値にすれば最後まで切り出してくれるはず.)  
(3)mode: rgb or flow  
(4)load_model:参照するモデル(default->rgb_charades.pt)  
(5)root:画像があるディレクトリ  
(6)save_dir:抽出した特徴量の保存先  

## run_preprocess.sh
(1)dir_video:抽出したい動画があるディレクトリ  
(2)extension_video:動画の拡張子  
(3)dir_log:抽出の進行状況を記録するlog.txtの出力先を指定  
(4)name_log:log.txt(固定で良い)  
