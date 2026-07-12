# Mipurin DressUp Studio

> [!NOTE]
> この試作リポジトリは、現在の開発対象から外れたため開発を停止しました。
> 主要コードと設定は、非公開の統合保管庫 `goroyattemiyo/project-vault` の
> `experiments/mipurin-dressup-studio/` に保存しています。
>
> 現行のミプリンUnity開発の正本：
> [`goroyattemiyo/mipurin-adventure-unity`](https://github.com/goroyattemiyo/mipurin-adventure-unity)
>
> この元リポジトリは、設計資料とコミット履歴を残す参照用アーカイブです。

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

## 最初のMVP

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

## ディレクトリ構成

```text
.
├─ README.md
├─ docs/
├─ prompts/
├─ config/
├─ tools/
├─ unity/Runtime/
└─ .github/ISSUE_TEMPLATE/
```

## 運用ルール

- 元PNGは `assets/source/` に保存する
- AI生成・補正済みのパーツは `assets/generated/` に保存する
- Unity投入用の確定パーツは `assets/unity-ready/` に保存する
- 全パーツは同一キャンバスサイズに揃える
- パーツ名は小文字スネークケースで統一する
- 表情・口・目・羽・髪はUnity側で差し替えやすいように別名管理する

## 注意

このリポジトリは、PNG1枚から完全自動で完璧なLive2Dモデルを作るものではありません。
目的は、**AI生成・半自動補助・人間の確認修正を組み合わせて、Unityで扱いやすいミプリン用パーツ素材を安定して作ること**です。