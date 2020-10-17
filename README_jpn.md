# Video-Feature-Extraction
このリポジトリは動画の特徴抽出器のコードをまとめたものです。  
ベースとなっている手法は[こちら](https://arxiv.org/abs/1705.07750)で、自分で使うために書き直しました。  
実行のための手順を記してあります。  

# 編集が必要なコードについて  
## preprocess.sh
前提として動画からフレームの切り出しをするのに[ffmpeg](https://ffmpeg.org/)を使用します。  
こちらは参考になる[記事(例)](https://qiita.com/cha84rakanal/items/e84fe4eb6fbe2ae13fd8)がそこそこあるので参考にしてください。  
1.settings  
(1)CONVERT_VIDEO_TO_IMG = true or false  
(2)CROP_VIDEO = true or false
(3)RUN_I3D_PYTORCH = true(固定)

2.video information

## run_preprocess.sh
