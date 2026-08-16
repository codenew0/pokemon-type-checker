# Pokémon Type Matchup Analyzer

ポケモンのタイプ相性をすばやく確認できる、シンプルなデスクトップアプリです。相手のタイプと使用する技タイプを選ぶと、攻撃倍率、防御相性、おすすめのタイプを一覧表示します。

The UI can be switched between Japanese and English from the language menu.

## 主な機能

- 相手のタイプを1〜2個選択
- 相手の技タイプを1〜4個選択
- 4倍、2倍、等倍、0.5倍、0.25倍、無効の攻撃倍率を表示
- 選択したすべての技に対する防御相性を分析
- 攻撃面・防御面・タイプ一致を想定したおすすめを表示
- 日本語／英語のUI切り替え
- 『ポケットモンスター スカーレット・バイオレット』形式のタイプバッジを使用
- インターネット接続なしで動作

## 必要環境

- Python 3.8以降
- Tkinter

外部Pythonパッケージは必要ありません。通常、Windows版PythonにはTkinterが含まれています。

## 起動方法

リポジトリを取得し、プロジェクトディレクトリで次を実行します。

```powershell
python typeChecker.py
```

Windowsで `python` コマンドが利用できない場合：

```powershell
py typeChecker.py
```

## 使い方

1. 左上から相手のポケモンタイプを選択します。
2. 左下から相手が使用する技タイプを選択します。
3. 「分析する」または「Analyze」を押します。
4. 右側におすすめと詳しい相性が表示されます。

右上のプルダウンから、日本語とEnglishをいつでも切り替えられます。選択内容と分析結果は切り替え後も維持されます。

## 防御相性の判定

複数の技タイプを選択した場合、各防御タイプは次のルールで分類されます。

| 分類 | 条件 |
|---|---|
| ばつぐん | 1つでも2倍以上で受ける技がある |
| 無効 | 選択したすべての技が0倍 |
| いまいち | 選択したすべての技が0.5倍以下 |
| 等倍 | 上記以外（耐性と等倍が混在する場合を含む） |

例えば「でんき」と「ノーマル」に対する「じめん」は、でんきを無効化できますがノーマルは等倍なので、全体評価は「等倍」になります。

## 対象範囲

このアプリは、18タイプの基本的な相性を確認するためのツールです。実際のポケモン、複合タイプの防御候補、特性、覚える技、能力値、持ち物、天候などは考慮しません。

## Project structure

```text
pokemon/
├─ typeChecker.py
└─ assets/
   ├─ type_icons/      # English type badges
   └─ type_icons_ja/   # Japanese type badges
```

## Type badge assets

英語タイプバッジは [PokeAPI/sprites](https://github.com/PokeAPI/sprites/tree/master/sprites/types/generation-ix/scarlet-violet) の画像を利用しています。日本語タイプバッジは、同じシンボルと配色を保ってラベルを日本語化したものです。

Pokémon and Pokémon character names are trademarks of Nintendo, Game Freak, and Creatures. This is an unofficial fan-made tool and is not affiliated with or endorsed by them.
