import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import List, Dict, Set

class PokemonTypeRecommender:
    def __init__(self):
        # ポケモンタイプの定義
        self.types = [
            "ノーマル", "ほのお", "みず", "でんき", "くさ", "こおり",
            "かくとう", "どく", "じめん", "ひこう", "エスパー", "むし",
            "いわ", "ゴースト", "ドラゴン", "あく", "はがね", "フェアリー"
        ]
        
        # タイプごとの色
        self.type_colors = {
            "ノーマル": "#A8A878", "ほのお": "#F08030", "みず": "#6890F0", 
            "でんき": "#F8D030", "くさ": "#78C850", "こおり": "#98D8D8",
            "かくとう": "#C03028", "どく": "#A040A0", "じめん": "#E0C068", 
            "ひこう": "#A890F0", "エスパー": "#F85888", "むし": "#A8B820",
            "いわ": "#B8A038", "ゴースト": "#705898", "ドラゴン": "#7038F8", 
            "あく": "#705848", "はがね": "#B8B8D0", "フェアリー": "#EE99AC"
        }

        # PokeAPIのタイプID（SVタイプアイコンのファイル名に対応）
        self.type_ids = {
            "ノーマル": 1, "かくとう": 2, "ひこう": 3, "どく": 4,
            "じめん": 5, "いわ": 6, "むし": 7, "ゴースト": 8,
            "はがね": 9, "ほのお": 10, "みず": 11, "くさ": 12,
            "でんき": 13, "エスパー": 14, "こおり": 15,
            "ドラゴン": 16, "あく": 17, "フェアリー": 18
        }
        self.type_names_en = {
            "ノーマル": "Normal", "ほのお": "Fire", "みず": "Water",
            "でんき": "Electric", "くさ": "Grass", "こおり": "Ice",
            "かくとう": "Fighting", "どく": "Poison", "じめん": "Ground",
            "ひこう": "Flying", "エスパー": "Psychic", "むし": "Bug",
            "いわ": "Rock", "ゴースト": "Ghost", "ドラゴン": "Dragon",
            "あく": "Dark", "はがね": "Steel", "フェアリー": "Fairy"
        }
        
        # タイプ相性表（攻撃側タイプ: {防御側タイプ: 倍率}）
        self.type_effectiveness = {
            "ノーマル": {"いわ": 0.5, "ゴースト": 0, "はがね": 0.5},
            "ほのお": {"ほのお": 0.5, "みず": 0.5, "くさ": 2, "こおり": 2, "むし": 2, "いわ": 0.5, "ドラゴン": 0.5, "はがね": 2},
            "みず": {"ほのお": 2, "みず": 0.5, "くさ": 0.5, "じめん": 2, "いわ": 2, "ドラゴン": 0.5},
            "でんき": {"みず": 2, "でんき": 0.5, "くさ": 0.5, "じめん": 0, "ひこう": 2, "ドラゴン": 0.5},
            "くさ": {"ほのお": 0.5, "みず": 2, "くさ": 0.5, "どく": 0.5, "じめん": 2, "ひこう": 0.5, "むし": 0.5, "いわ": 2, "ドラゴン": 0.5, "はがね": 0.5},
            "こおり": {"ほのお": 0.5, "みず": 0.5, "くさ": 2, "こおり": 0.5, "じめん": 2, "ひこう": 2, "ドラゴン": 2, "はがね": 0.5},
            "かくとう": {"ノーマル": 2, "こおり": 2, "どく": 0.5, "ひこう": 0.5, "エスパー": 0.5, "むし": 0.5, "いわ": 2, "ゴースト": 0, "あく": 2, "はがね": 2, "フェアリー": 0.5},
            "どく": {"くさ": 2, "どく": 0.5, "じめん": 0.5, "いわ": 0.5, "ゴースト": 0.5, "はがね": 0, "フェアリー": 2},
            "じめん": {"ほのお": 2, "でんき": 2, "くさ": 0.5, "どく": 2, "ひこう": 0, "むし": 0.5, "いわ": 2, "はがね": 2},
            "ひこう": {"でんき": 0.5, "くさ": 2, "かくとう": 2, "むし": 2, "いわ": 0.5, "はがね": 0.5},
            "エスパー": {"かくとう": 2, "どく": 2, "エスパー": 0.5, "あく": 0, "はがね": 0.5},
            "むし": {"ほのお": 0.5, "くさ": 2, "かくとう": 0.5, "どく": 0.5, "ひこう": 0.5, "エスパー": 2, "ゴースト": 0.5, "あく": 2, "はがね": 0.5, "フェアリー": 0.5},
            "いわ": {"ほのお": 2, "こおり": 2, "かくとう": 0.5, "じめん": 0.5, "ひこう": 2, "むし": 2, "はがね": 0.5},
            "ゴースト": {"ノーマル": 0, "エスパー": 2, "ゴースト": 2, "あく": 0.5},
            "ドラゴン": {"ドラゴン": 2, "はがね": 0.5, "フェアリー": 0},
            "あく": {"かくとう": 0.5, "エスパー": 2, "ゴースト": 2, "あく": 0.5, "フェアリー": 0.5},
            "はがね": {"ほのお": 0.5, "みず": 0.5, "でんき": 0.5, "こおり": 2, "いわ": 2, "はがね": 0.5, "フェアリー": 2},
            "フェアリー": {"ほのお": 0.5, "かくとう": 2, "どく": 0.5, "ドラゴン": 2, "あく": 2, "はがね": 0.5}
        }
    
    def get_attack_effectiveness(self, attack_type: str, defend_types: List[str]) -> float:
        """攻撃タイプが防御タイプに与えるダメージ倍率を計算"""
        multiplier = 1.0
        for defend_type in defend_types:
            if defend_type in self.type_effectiveness.get(attack_type, {}):
                multiplier *= self.type_effectiveness[attack_type][defend_type]
        return multiplier
    
    def analyze_enemy(self, enemy_types: List[str]) -> Dict[float, List[str]]:
        """敵タイプに対する各攻撃タイプの効果を分析"""
        effectiveness = {4.0: [], 2.0: [], 1.0: [], 0.5: [], 0.25: [], 0.0: []}
        
        for attack_type in self.types:
            multiplier = self.get_attack_effectiveness(attack_type, enemy_types)
            if multiplier in effectiveness:
                effectiveness[multiplier].append(attack_type)
            else:
                effectiveness[multiplier] = [attack_type]
        
        return effectiveness
    
    def analyze_defense(self, enemy_move_types: List[str]) -> Dict[str, List[str]]:
        """敵の技に対する各防御タイプの耐性を分析"""
        defense_analysis = {
            "ばつぐん": set(),
            "有効": set(),
            "いまいち": set(),
            "無効": set()
        }
        
        for defend_type in self.types:
            damages = [
                self.get_attack_effectiveness(move_type, [defend_type])
                for move_type in enemy_move_types
            ]

            # 複数の技をまとめて評価するため、最も大きい倍率を基準にする。
            # 「無効」「いまいち」は、選択された全技に対して成立する場合だけ表示する。
            max_damage = max(damages, default=1.0)
            if max_damage >= 2.0:
                defense_analysis["ばつぐん"].add(defend_type)
            elif max_damage == 0:
                defense_analysis["無効"].add(defend_type)
            elif max_damage <= 0.5:
                defense_analysis["いまいち"].add(defend_type)
            else:
                defense_analysis["有効"].add(defend_type)
        
        # setの列挙順に依存せず、タイプ一覧と同じ順序で表示する。
        return {
            category: [type_name for type_name in self.types if type_name in values]
            for category, values in defense_analysis.items()
        }
    
    def recommend_pokemon(self, enemy_types: List[str], enemy_move_types: List[str]) -> Dict:
        """最適なポケモンタイプと技タイプを推奨"""
        attack_effectiveness = self.analyze_enemy(enemy_types)
        defense_analysis = self.analyze_defense(enemy_move_types)
        
        good_attack_types = set(attack_effectiveness[4.0] + attack_effectiveness[2.0])
        good_defense_types = set(defense_analysis["いまいち"] + defense_analysis["無効"])
        bad_defense_types = set(defense_analysis["ばつぐん"])
        
        recommended_pokemon_types = good_defense_types - bad_defense_types
        recommended_move_types = good_attack_types
        
        # タイプ一致を考慮した総合推奨（防御有利 ∩ 攻撃等倍以上）
        # 攻撃が等倍以上のタイプ（いまいち・無効でないタイプ）
        not_bad_attack_types = set()
        for attack_type in self.types:
            multiplier = self.get_attack_effectiveness(attack_type, enemy_types)
            if multiplier >= 1.0:  # 等倍以上
                not_bad_attack_types.add(attack_type)
        
        # 防御有利で、攻撃も等倍以上取れるタイプ
        balanced_types = good_defense_types & not_bad_attack_types
        
        return {
            "attack_effectiveness": attack_effectiveness,
            "defense_analysis": defense_analysis,
            "recommended_pokemon_types": [
                type_name for type_name in self.types
                if type_name in recommended_pokemon_types
            ],
            "recommended_move_types": [
                type_name for type_name in self.types
                if type_name in recommended_move_types
            ],
            "balanced_types": [
                type_name for type_name in self.types
                if type_name in balanced_types
            ]
        }


class TypeButton(tk.Button):
    """タイプ選択用のカスタムボタン"""
    def __init__(self, parent, type_name, color, command, type_icon=None):
        button_options = {
            # アイコン使用時はチェック領域を常時確保し、サイズ変化を防ぐ。
            "text": "✓" if type_icon else type_name,
            "bg": "#ffffff" if type_icon else color,
            "activebackground": "#e8f3ff",
            "activeforeground": "white",
            "fg": "white",
            "font": ('Arial', 10, 'bold'),
            "relief": tk.RAISED,
            "bd": 2,
            "cursor": 'hand2',
            "command": command,
            "takefocus": True,
            "highlightthickness": 2,
            "highlightbackground": "#d7dde5",
            "highlightcolor": "#2478c5"
        }
        if type_icon:
            button_options.update({
                "image": type_icon,
                "compound": tk.LEFT,
                "width": 150,
                "height": 30,
                "padx": 0,
                "pady": 0
            })
        else:
            button_options.update({"width": 8, "height": 1})

        super().__init__(
            parent,
            **button_options
        )
        self.type_name = type_name
        self.type_icon = type_icon
        self.selected = False
        self.default_bg = "#ffffff" if type_icon else color
        self.selected_bg = self._darken_color(color)
        
    def _darken_color(self, hex_color):
        """色を暗くする"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.5))
        g = max(0, int(g * 0.5))
        b = max(0, int(b * 0.5))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def toggle(self):
        """選択状態を切り替え"""
        self.selected = not self.selected
        if self.selected:
            self.config(
                relief=tk.SUNKEN, 
                bg="#b9dcfa" if self.type_icon else self.selected_bg,
                activebackground="#b9dcfa",
                activeforeground="#075a9c",
                text="✓" if self.type_icon else f"✓ {self.type_name}",
                fg="#075a9c" if self.type_icon else "white",
                font=('Arial', 10, 'bold'),
                bd=2,
                highlightbackground="#075a9c"
            )
        else:
            self.config(
                relief=tk.RAISED, 
                bg=self.default_bg,
                activebackground="#e8f3ff",
                activeforeground=self.default_bg if self.type_icon else "white",
                text="✓" if self.type_icon else self.type_name,
                fg=self.default_bg if self.type_icon else "white",
                font=('Arial', 10, 'bold'),
                bd=2,
                highlightbackground="#d7dde5"
            )
    
    def reset(self):
        """選択状態をリセット"""
        self.selected = False
        self.config(
            relief=tk.RAISED, 
            bg=self.default_bg,
            activebackground="#e8f3ff",
            activeforeground=self.default_bg if self.type_icon else "white",
            text="✓" if self.type_icon else self.type_name,
            fg=self.default_bg if self.type_icon else "white",
            bd=2,
            highlightbackground="#d7dde5"
        )


class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1280x800")
        self.root.minsize(1120, 720)
        self.root.configure(bg='#f0f0f0')
        
        self.recommender = PokemonTypeRecommender()
        self.language = "ja"
        self.language_var = tk.StringVar(value="日本語")
        self.type_icons = {
            "ja": self.load_type_icons("type_icons_ja"),
            "en": self.load_type_icons("type_icons")
        }
        self.enemy_type_buttons = []
        self.enemy_move_buttons = []
        self.texts = {
            "ja": {
                "window_title": "ポケモンタイプ対戦分析ツール",
                "app_title": "🎮 ポケモンタイプ対戦分析",
                "enemy_types": "🎯 敵のポケモンタイプ（1〜2個選択）",
                "enemy_moves": "⚡ 敵の技タイプ（1〜4個選択）",
                "analyze": "⚔️ 分析する", "reset": "🔄 リセット",
                "results": "📊 分析結果",
                "initial_1": "　　敵のタイプと技を選択して",
                "initial_2": "　　「分析する」ボタンを押してください",
                "hint": "　　💡 ヒント：",
                "hint_type": "　　• 敵のタイプは1〜2個選択可能",
                "hint_move": "　　• 敵の技は1〜4個選択可能",
                "hint_toggle": "　　• ボタンをクリックして選択/解除",
                "need_type": "⚠️ 敵のタイプを選択してください",
                "need_move": "⚠️ 敵の技タイプを選択してください",
                "strategy": "　✨ おすすめの戦略",
                "balanced": "🌟 タイプ一致技を使う場合の総合おすすめ",
                "balanced_desc1": "　→ 敵の技を半減でき、等倍以上のダメージも出せます",
                "balanced_desc2": "　　 タイプ一致補正（1.5倍）で安定した戦いができます！",
                "defense_recommend": "🎯 おすすめポケモンタイプ（防御面）",
                "defense_desc": "　→ 敵の技を受けにくく安全です",
                "none": "　該当なし",
                "defense_none": "　→ 防御面で完全に有利なタイプはありません",
                "move_recommend": "⚔️ おすすめ技タイプ（攻撃面）",
                "move_desc": "　→ 敵に効果的なダメージを与えられます",
                "enemy_info": "　敵の情報", "type_label": "タイプ： ", "move_label": "技　　： ",
                "damage_dealt": "　⚔️ 敵に与えるダメージ",
                "damage4": "🔥 4倍ダメージ！", "damage2": "⚡ 2倍ダメージ（効果抜群）",
                "damage1": "➖ 等倍ダメージ", "damage05": "💧 0.5倍（いまいち）",
                "damage025": "💧 0.25倍（とても いまいち）", "damage0": "🚫 無効（ダメージなし）",
                "damage_received": "　🛡️ 敵の技から受けるダメージ",
                "defense0": "🚫 無効（ダメージ0倍）", "defense05": "🛡️ いまいち（0.5倍以下）",
                "defense1": "➖ 等倍", "defense2": "⚠️ ばつぐん（2倍以上）"
            },
            "en": {
                "window_title": "Pokémon Type Matchup Analyzer",
                "app_title": "🎮 Pokémon Type Matchup Analyzer",
                "enemy_types": "🎯 Opponent's Type (select 1–2)",
                "enemy_moves": "⚡ Opponent's Move Types (select 1–4)",
                "analyze": "⚔️ Analyze", "reset": "🔄 Reset",
                "results": "📊 Analysis Results",
                "initial_1": "　Select the opponent's types and moves,",
                "initial_2": "　then press “Analyze.”",
                "hint": "　💡 Tips:",
                "hint_type": "　• Select one or two opponent types",
                "hint_move": "　• Select up to four move types",
                "hint_toggle": "　• Click a button to select or deselect it",
                "need_type": "⚠️ Select at least one opponent type.",
                "need_move": "⚠️ Select at least one opponent move type.",
                "strategy": "　✨ Recommended Strategy",
                "balanced": "🌟 Best all-round STAB type",
                "balanced_desc1": "　→ Resists every selected move and deals at least neutral damage",
                "balanced_desc2": "　　 STAB (×1.5) provides reliable damage.",
                "defense_recommend": "🎯 Recommended Pokémon Types (Defense)",
                "defense_desc": "　→ These types safely resist every selected move.",
                "none": "　None",
                "defense_none": "　→ No type has a favorable matchup against every selected move.",
                "move_recommend": "⚔️ Recommended Move Types (Offense)",
                "move_desc": "　→ These move types deal super-effective damage.",
                "enemy_info": "　Opponent", "type_label": "Types: ", "move_label": "Moves: ",
                "damage_dealt": "　⚔️ Damage Dealt",
                "damage4": "🔥 ×4 damage!", "damage2": "⚡ ×2 damage (super effective)",
                "damage1": "➖ ×1 damage (neutral)", "damage05": "💧 ×0.5 damage (not very effective)",
                "damage025": "💧 ×0.25 damage", "damage0": "🚫 No effect (×0)",
                "damage_received": "　🛡️ Damage Taken from Selected Moves",
                "defense0": "🚫 Immune to every move (×0)", "defense05": "🛡️ Resists every move (×0.5 or less)",
                "defense1": "➖ Neutral or mixed matchup", "defense2": "⚠️ Weak to at least one move (×2 or more)"
            }
        }
        
        self.create_widgets()

    def tr(self, key):
        return self.texts[self.language][key]

    def load_type_icons(self, folder_name):
        """プロジェクト内のSVタイプアイコンを読み込む。"""
        icon_dir = Path(__file__).resolve().parent / "assets" / folder_name
        icons = {}
        for type_name, type_id in self.recommender.type_ids.items():
            icon_path = icon_dir / f"{type_id}.png"
            if icon_path.exists():
                # 元画像は200x40。140x28に縮小して、文字とシンボルを見やすくする。
                source = tk.PhotoImage(file=str(icon_path))
                icons[type_name] = source.zoom(7, 7).subsample(10, 10)
        return icons

    def change_language(self, event=None):
        """選択内容を保持したまま表示言語を切り替える。"""
        new_language = "ja" if self.language_var.get() == "日本語" else "en"
        if new_language == self.language:
            return

        selected_types = [b.type_name for b in self.enemy_type_buttons if b.selected]
        selected_moves = [b.type_name for b in self.enemy_move_buttons if b.selected]
        self.language = new_language

        for widget in self.root.winfo_children():
            widget.destroy()
        self.enemy_type_buttons = []
        self.enemy_move_buttons = []
        self.create_widgets()

        for button in self.enemy_type_buttons:
            if button.type_name in selected_types:
                button.toggle()
        for button in self.enemy_move_buttons:
            if button.type_name in selected_moves:
                button.toggle()
        if selected_types and selected_moves:
            self.analyze()

    def insert_type_names(self, type_names, tag=None):
        """分析結果へ、現在の言語に合わせたタイプ名をコンパクトに表示する。"""
        labels = [
            type_name if self.language == "ja"
            else self.recommender.type_names_en[type_name]
            for type_name in type_names
        ]
        self.result_text.insert(tk.END, ", ".join(labels) + "\n", tag)
    
    def create_widgets(self):
        self.root.title(self.tr("window_title"))

        language_frame = tk.Frame(self.root, bg='#f0f0f0')
        language_frame.pack(fill=tk.X, padx=20, pady=(12, 0))
        language_box = ttk.Combobox(
            language_frame,
            textvariable=self.language_var,
            values=("日本語", "English"),
            state="readonly",
            width=11,
            font=('Arial', 11)
        )
        language_box.pack(side=tk.RIGHT)
        language_box.bind("<<ComboboxSelected>>", self.change_language)
        tk.Label(
            language_frame,
            text="🌐 言語 / Language",
            font=('Arial', 10, 'bold'),
            bg='#f0f0f0',
            fg='#34495e'
        ).pack(side=tk.RIGHT, padx=(0, 8))

        # メインコンテナ
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(8, 20))
        
        # 左側：入力エリア
        left_frame = tk.Frame(main_container, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # タイトル
        title_label = tk.Label(
            left_frame,
            text=self.tr("app_title"),
            font=('Arial', 18, 'bold'),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # 敵のタイプ選択エリア
        self.create_enemy_type_section(left_frame)
        
        # 敵の技タイプ選択エリア
        self.create_enemy_move_section(left_frame)
        
        # ボタンエリア
        button_frame = tk.Frame(left_frame, bg='#f0f0f0')
        button_frame.pack(pady=20)
        
        analyze_btn = tk.Button(
            button_frame,
            text=self.tr("analyze"),
            command=self.analyze,
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(
            button_frame,
            text=self.tr("reset"),
            command=self.reset_all,
            font=('Arial', 14, 'bold'),
            bg='#95a5a6',
            fg='white',
            width=12,
            height=2,
            relief=tk.RAISED,
            bd=3,
            cursor='hand2'
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 右側：結果表示エリア
        right_frame = tk.Frame(main_container, bg='white', relief=tk.SOLID, bd=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        result_title = tk.Label(
            right_frame,
            text=self.tr("results"),
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        result_title.pack(pady=10)
        
        # スクロールバー付きテキストエリア
        text_frame = tk.Frame(right_frame, bg='white')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(
            text_frame,
            yscrollcommand=scrollbar.set,
            font=('Arial', 11),
            wrap=tk.WORD,
            bg='#fafafa',
            relief=tk.FLAT,
            padx=10,
            pady=10
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # テキストタグの設定
        self.result_text.tag_config("title", font=('Arial', 14, 'bold'), foreground='#2c3e50', spacing3=10)
        self.result_text.tag_config("section", font=('Arial', 12, 'bold'), foreground='#34495e', spacing1=5, spacing3=5)
        self.result_text.tag_config("damage4x", font=('Arial', 11, 'bold'), foreground='#e74c3c')
        self.result_text.tag_config("damage2x", font=('Arial', 11), foreground='#e67e22')
        self.result_text.tag_config("damage1x", font=('Arial', 11), foreground='#7f8c8d')
        self.result_text.tag_config("damage05x", font=('Arial', 11), foreground='#3498db')
        self.result_text.tag_config("damage0x", font=('Arial', 11), foreground='#95a5a6')
        self.result_text.tag_config("recommend", font=('Arial', 12, 'bold'), foreground='#27ae60', spacing3=5)
        self.result_text.tag_config("best", font=('Arial', 13, 'bold'), foreground='#d35400', spacing3=5)
        self.result_text.tag_config("highlight", background='#fff9c4')
        self.result_text.tag_config("best_highlight", background='#ffeb3b', font=('Arial', 12, 'bold'))
        
        # 初期メッセージ
        self.show_initial_message()
    
    def create_enemy_type_section(self, parent):
        """敵のタイプ選択セクション"""
        section_frame = tk.LabelFrame(
            parent,
            text=self.tr("enemy_types"),
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50',
            relief=tk.SOLID,
            bd=2,
            padx=15,
            pady=15
        )
        section_frame.pack(fill=tk.BOTH, pady=(0, 15))
        
        # タイプボタングリッド
        grid_frame = tk.Frame(section_frame, bg='white')
        grid_frame.pack()
        
        for i, type_name in enumerate(self.recommender.types):
            row = i // 4
            col = i % 4
            
            btn = TypeButton(
                grid_frame,
                type_name,
                self.recommender.type_colors[type_name],
                lambda t=type_name: self.toggle_enemy_type(t),
                self.type_icons[self.language].get(type_name)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.enemy_type_buttons.append(btn)
    
    def create_enemy_move_section(self, parent):
        """敵の技タイプ選択セクション"""
        section_frame = tk.LabelFrame(
            parent,
            text=self.tr("enemy_moves"),
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50',
            relief=tk.SOLID,
            bd=2,
            padx=15,
            pady=15
        )
        section_frame.pack(fill=tk.BOTH)
        
        # タイプボタングリッド
        grid_frame = tk.Frame(section_frame, bg='white')
        grid_frame.pack()
        
        for i, type_name in enumerate(self.recommender.types):
            row = i // 4
            col = i % 4
            
            btn = TypeButton(
                grid_frame,
                type_name,
                self.recommender.type_colors[type_name],
                lambda t=type_name: self.toggle_enemy_move(t),
                self.type_icons[self.language].get(type_name)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.enemy_move_buttons.append(btn)
    
    def toggle_enemy_type(self, type_name):
        """敵のタイプ選択をトグル"""
        btn = next(b for b in self.enemy_type_buttons if b.type_name == type_name)
        
        selected_count = sum(1 for b in self.enemy_type_buttons if b.selected)
        
        if btn.selected or selected_count < 2:
            btn.toggle()
    
    def toggle_enemy_move(self, type_name):
        """敵の技タイプ選択をトグル"""
        btn = next(b for b in self.enemy_move_buttons if b.type_name == type_name)
        
        selected_count = sum(1 for b in self.enemy_move_buttons if b.selected)
        
        if btn.selected or selected_count < 4:
            btn.toggle()
    
    def reset_all(self):
        """全ての選択をリセット"""
        for btn in self.enemy_type_buttons + self.enemy_move_buttons:
            btn.reset()
        self.show_initial_message()
    
    def show_initial_message(self):
        """初期メッセージを表示"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "\n\n\n")
        self.result_text.insert(tk.END, self.tr("initial_1") + "\n", "title")
        self.result_text.insert(tk.END, self.tr("initial_2") + "\n\n", "title")
        self.result_text.insert(tk.END, self.tr("hint") + "\n", "section")
        self.result_text.insert(tk.END, self.tr("hint_type") + "\n")
        self.result_text.insert(tk.END, self.tr("hint_move") + "\n")
        self.result_text.insert(tk.END, self.tr("hint_toggle") + "\n")
    
    def analyze(self):
        """分析を実行"""
        # 選択されたタイプを取得
        enemy_types = [b.type_name for b in self.enemy_type_buttons if b.selected]
        enemy_move_types = [b.type_name for b in self.enemy_move_buttons if b.selected]
        
        if not enemy_types:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n\n")
            self.result_text.insert(tk.END, self.tr("need_type") + "\n", "section")
            return
        
        if not enemy_move_types:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n\n")
            self.result_text.insert(tk.END, self.tr("need_move") + "\n", "section")
            return
        
        # 分析実行
        result = self.recommender.recommend_pokemon(enemy_types, enemy_move_types)
        
        # 結果表示
        self.display_results(enemy_types, enemy_move_types, result)
    
    def display_results(self, enemy_types, enemy_move_types, result):
        """結果を表示"""
        self.result_text.delete(1.0, tk.END)
                
        # 推奨
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, self.tr("strategy") + "\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        
        # タイプ一致を考慮した総合推奨
        if result["balanced_types"]:
            self.result_text.insert(tk.END, self.tr("balanced") + "\n", "best")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(result["balanced_types"], "best_highlight")
            self.result_text.insert(tk.END, self.tr("balanced_desc1") + "\n")
            self.result_text.insert(tk.END, self.tr("balanced_desc2") + "\n\n")
        
        self.result_text.insert(tk.END, self.tr("defense_recommend") + "\n", "recommend")
        if result["recommended_pokemon_types"]:
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(result["recommended_pokemon_types"], "highlight")
            self.result_text.insert(tk.END, self.tr("defense_desc") + "\n\n")
        else:
            self.result_text.insert(tk.END, self.tr("none") + "\n")
            self.result_text.insert(tk.END, self.tr("defense_none") + "\n\n")
        
        self.result_text.insert(tk.END, self.tr("move_recommend") + "\n", "recommend")
        if result["recommended_move_types"]:
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(result["recommended_move_types"], "highlight")
            self.result_text.insert(tk.END, self.tr("move_desc") + "\n\n")
        else:
            self.result_text.insert(tk.END, self.tr("none") + "\n\n")
        
        # 敵情報
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, self.tr("enemy_info") + "\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        self.result_text.insert(tk.END, self.tr("type_label"), "section")
        self.insert_type_names(enemy_types, "section")
        self.result_text.insert(tk.END, self.tr("move_label"), "section")
        self.insert_type_names(enemy_move_types, "section")
        self.result_text.insert(tk.END, "\n")
        
        # 攻撃効果
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, self.tr("damage_dealt") + "\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        
        attack_eff = result["attack_effectiveness"]
        
        if attack_eff[4.0]:
            self.result_text.insert(tk.END, self.tr("damage4") + "\n", "damage4x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(attack_eff[4.0], "damage4x")
            self.result_text.insert(tk.END, "\n")
        
        if attack_eff[2.0]:
            self.result_text.insert(tk.END, self.tr("damage2") + "\n", "damage2x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(attack_eff[2.0], "damage2x")
            self.result_text.insert(tk.END, "\n")
        
        if attack_eff[1.0]:
            self.result_text.insert(tk.END, self.tr("damage1") + "\n", "damage1x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(attack_eff[1.0], "damage1x")
            self.result_text.insert(tk.END, "\n")
        
        if attack_eff[0.5]:
            self.result_text.insert(tk.END, self.tr("damage05") + "\n", "damage05x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(attack_eff[0.5], "damage05x")
            self.result_text.insert(tk.END, "\n")
        
        if attack_eff[0.25]:
            self.result_text.insert(tk.END, self.tr("damage025") + "\n", "damage05x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(attack_eff[0.25], "damage05x")
            self.result_text.insert(tk.END, "\n")
        
        if attack_eff[0.0]:
            self.result_text.insert(tk.END, self.tr("damage0") + "\n", "damage0x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(attack_eff[0.0], "damage0x")
            self.result_text.insert(tk.END, "\n")
        
        # 防御効果
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, self.tr("damage_received") + "\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        
        defense_ana = result["defense_analysis"]
        
        if defense_ana["無効"]:
            self.result_text.insert(tk.END, self.tr("defense0") + "\n", "damage0x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(defense_ana["無効"], "damage0x")
            self.result_text.insert(tk.END, "\n")
        
        if defense_ana["いまいち"]:
            self.result_text.insert(tk.END, self.tr("defense05") + "\n", "damage05x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(defense_ana["いまいち"], "damage05x")
            self.result_text.insert(tk.END, "\n")
        
        if defense_ana["有効"]:
            self.result_text.insert(tk.END, self.tr("defense1") + "\n", "damage1x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(defense_ana["有効"], "damage1x")
            self.result_text.insert(tk.END, "\n")
        
        if defense_ana["ばつぐん"]:
            self.result_text.insert(tk.END, self.tr("defense2") + "\n", "damage2x")
            self.result_text.insert(tk.END, "　")
            self.insert_type_names(defense_ana["ばつぐん"], "damage2x")
            self.result_text.insert(tk.END, "\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()
