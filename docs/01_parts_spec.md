# 01. ミプリン用パーツ分け仕様書

## 目的

Unityでミプリンのお着替え、髪色変更、ゆらゆら動作、羽の動き、まばたき、会話演出、表情変更、スクショ保存、RPG連動を行うための素材仕様です。

## 基本方針

すべてのPNGパーツは同じ透明キャンバスで管理します。Unityでは同じ座標に重ねて表示し、必要なパーツだけ差し替えます。

## 推奨キャンバス

```text
2048 x 2048 px
背景透明
PNG
sRGB
```

## レイヤー順

```text
background
hair_back
wing_left
wing_right
base
outfit
face
eyes
lip_sync
hair_front
accessory_body
accessory_head
effect_front
ui
```

## 最小パーツ

```text
base
face
hair_back
hair_front
eyes_open
eyes_closed
lip_sync_close
lip_sync_small
lip_sync_open
wing_left
wing_right
outfit_default
accessory_head_none
accessory_body_none
```

## 髪色差分

```text
pink
blonde
mint
lavender
skyblue
```

## 重要ルール

- 全パーツのキャンバスサイズを揃える
- 中心位置を揃える
- 透明余白を揃える
- 羽は左右別にする
- 髪、衣装、アクセサリーは差し替え前提で分ける
- 目と会話用パーツは表情差分として独立させる
- AI補完部分は必ず目視確認する
- 元のミプリンらしさとかわいさを最優先する
