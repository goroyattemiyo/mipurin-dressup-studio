# 04. Unity読み込み・実装仕様

## 目的

作成したミプリンの透明PNGパーツをUnityに読み込み、着せ替え、ゆらゆら、まばたき、会話演出を実現する。

## Prefab構成

```text
Player_Mipurin_DressUp
├─ HairBack
├─ WingLeft
├─ WingRight
├─ Base
├─ Outfit
├─ Face
├─ Eyes
├─ LipSync
├─ Blush
├─ HairFront
├─ AccessoryBody
├─ AccessoryHead
└─ EffectFront
```

## Sorting Order

```text
HairBack: 0
WingLeft: 5
WingRight: 5
Base: 10
Outfit: 20
Face: 30
Eyes: 40
LipSync: 41
Blush: 42
HairFront: 50
AccessoryBody: 60
AccessoryHead: 70
EffectFront: 100
```

## Assets配置

```text
Assets/MipurinDressUp/Sprites/
Assets/MipurinDressUp/Prefabs/
Assets/MipurinDressUp/Scripts/
Assets/MipurinDressUp/Scenes/
Assets/MipurinDressUp/ScriptableObjects/
```

## 最初に作るScene

```text
MipurinDressUpRoom.unity
```

画面構成:

```text
中央: ミプリン
下部: セリフ欄
右側: 着せ替えカテゴリ
左側: 表情ボタン
上部: スクショ / 保存 / リセット
```

## 実装順

```text
1. SpriteRendererでパーツを重ねる
2. Sorting Orderを設定する
3. Inspectorから差し替え確認
4. DressupControllerで差し替え処理を作る
5. Idleふわふわを入れる
6. 羽パタを入れる
7. まばたきを入れる
8. 会話演出を入れる
9. UIボタン接続
10. セーブ/ロード
11. スクショ保存
```
