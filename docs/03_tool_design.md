# 03. Python半自動ツール設計

## 目的

現在のPNG素材をUnityで扱いやすい状態に整える補助ツールを作る。

## MVPでやること

```text
1. 入力PNGを読み込む
2. 透明チャンネルを確認する
3. 表示領域を自動検出する
4. 指定キャンバスへ中央配置する
5. 整形済みPNGを保存する
6. manifest.jsonを出力する
```

## MVPでやらないこと

```text
意味単位の完全自動分解
隠れている部分の自動補完
Live2Dモデルの自動生成
```

## 推奨フォルダ

```text
assets/source/
assets/masks/
assets/generated/
assets/unity-ready/
assets/preview/
```

## コマンド例

```bash
python tools/splitter_mvp.py assets/source/mipurin_original.png --out assets/generated/test --canvas 2048
```

## 将来拡張

- 矩形指定での切り出し
- 手動マスク読み込み
- 合成プレビュー出力
- Unity用JSON出力
- 簡易GUI

## 注意

背景除去やAI補完は別工程にし、Pythonツールは整列、検査、保存を担当する。
