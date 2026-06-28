# Mipurin DressUp Studio

ミプリンRPGから派生する、**ミプリンお着替え・Live2D風ゆらゆらアプリ**用の素材分解・管理・Unity連携リポジトリです。

このリポジトリの目的は、現在のミプリンPNGをそのまま使い切るのではなく、Unity上で以下を実現できるようにすることです。

- 髪色変更
- 服・羽・帽子・アクセサリーの着せ替え
- ふわふわIdle
- 羽パタ
- まばたき
- 口パク
- 表情差分
- スクショ保存
- 将来的なRPG本編とのアイテム連動

## 方針

最初から完全自動のLive2D化を狙わず、まずは **PNGパーツ分け + Unity Transformアニメーション** で実用MVPを作ります。

```text
Phase 1: PNGパーツ分け
Phase 2: Unityで重ね表示
Phase 3: ふわふわ・羽パタ・まばたき・口パク
Phase 4: 着せ替えUI
Phase 5: セーブ・スクショ・RPG連動
Phase 6: 余裕があればUnity 2D Animation / Live2D Cubism検討
```

## リポジトリ名

```text
mipurin-dressup-studio
```

関連候補:

```text
mipurin-dressup-studio
mipurin-parts-lab
mipurin-live2d-like-kit
mipurin-avatar-room
```

## 最初のMVP

最初はこの範囲で十分です。

```text
ミプリン本体: 1体
髪色: 5種類
羽: 3種類
服: 5種類
帽子/頭アクセ: 5種類
表情: 通常 / 笑顔 / びっくり / 困り
口: 閉じ / 小開き / 開き / 笑い
背景: 3種類
```

組み合わせ例:

```text
5 hair colors × 3 wings × 5 outfits × 5 accessories = 375通り
```

表情や背景も含めると、見た目のバリエーションはさらに増えます。

## ディレクトリ構成

```text
.
├─ README.md
├─ docs/
│  ├─ 01_parts_spec.md
│  ├─ 02_generation_prompts.md
│  ├─ 03_tool_design.md
│  ├─ 04_unity_import_spec.md
│  └─ 05_github_setup.md
├─ prompts/
│  ├─ part_split_main_prompt.md
│  ├─ hair_color_variation_prompt.md
│  └─ outfit_item_prompt.md
├─ config/
│  ├─ parts_schema.example.json
│  └─ unity_layers.example.json
├─ tools/
│  ├─ README.md
│  ├─ requirements.txt
│  └─ splitter_mvp.py
├─ unity/
│  └─ Runtime/
│     ├─ MipurinDressupController.cs
│     ├─ MipurinTalkAnimator.cs
│     └─ MipurinPartItem.cs
├─ .github/
│  └─ ISSUE_TEMPLATE/
│     └─ task.md
├─ .gitignore
└─ .gitattributes
```

## 運用ルール

- 元PNGは `assets/source/` に保存する
- AI生成・補正済みのパーツは `assets/generated/` に保存する
- Unity投入用の確定パーツは `assets/unity-ready/` に保存する
- 全パーツは同一キャンバスサイズに揃える
- パーツ名は小文字スネークケースで統一する
- 表情・口・目・羽・髪はUnity側で差し替えやすいように別名管理する

## 最初にやること

```bash
git clone <your-repo-url>
cd mipurin-dressup-studio

python -m venv .venv
.venv\Scripts\activate

pip install -r tools/requirements.txt
```

PNGの透明余白とキャンバスを統一するだけなら:

```bash
python tools/splitter_mvp.py input.png --out assets/generated/test_parts --canvas 2048
```

## 注意

このリポジトリは、PNG1枚から完全自動で完璧なLive2Dモデルを作るものではありません。

目的は、**AI生成・半自動補助・人間の確認修正を組み合わせて、Unityで扱いやすいミプリン用パーツ素材を安定して作ること**です。
