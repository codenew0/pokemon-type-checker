import tkinter as tk
from tkinter import ttk
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
            max_damage = 0.0
            has_immunity = False
            
            for move_type in enemy_move_types:
                damage = self.get_attack_effectiveness(move_type, [defend_type])
                if damage == 0:
                    has_immunity = True
                max_damage = max(max_damage, damage)
            
            if has_immunity:
                defense_analysis["無効"].add(defend_type)
            elif max_damage >= 2.0:
                defense_analysis["ばつぐん"].add(defend_type)
            elif max_damage <= 0.5:
                defense_analysis["いまいち"].add(defend_type)
            else:
                defense_analysis["有効"].add(defend_type)
        
        return {k: list(v) for k, v in defense_analysis.items()}
    
    def recommend_pokemon(self, enemy_types: List[str], enemy_move_types: List[str]) -> Dict:
        """最適なポケモンタイプと技タイプを推奨"""
        attack_effectiveness = self.analyze_enemy(enemy_types)
        defense_analysis = self.analyze_defense(enemy_move_types)
        
        good_attack_types = set(attack_effectiveness[4.0] + attack_effectiveness[2.0])
        good_defense_types = set(defense_analysis["いまいち"] + defense_analysis["無効"])
        bad_defense_types = set(defense_analysis["ばつぐん"])
        
        recommended_pokemon_types = good_defense_types - bad_defense_types
        recommended_move_types = good_attack_types
        
        return {
            "attack_effectiveness": attack_effectiveness,
            "defense_analysis": defense_analysis,
            "recommended_pokemon_types": list(recommended_pokemon_types),
            "recommended_move_types": list(recommended_move_types)
        }


class TypeButton(tk.Button):
    """タイプ選択用のカスタムボタン"""
    def __init__(self, parent, type_name, color, command):
        super().__init__(
            parent,
            text=type_name,
            bg=color,
            fg='white',
            font=('Arial', 10, 'bold'),
            width=8,
            height=1,
            relief=tk.RAISED,
            bd=2,
            cursor='hand2',
            command=command
        )
        self.type_name = type_name
        self.selected = False
        self.default_bg = color
        self.selected_bg = self._darken_color(color)
        
    def _darken_color(self, hex_color):
        """色を暗くする"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = max(0, int(r * 0.7))
        g = max(0, int(g * 0.7))
        b = max(0, int(b * 0.7))
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def toggle(self):
        """選択状態を切り替え"""
        self.selected = not self.selected
        if self.selected:
            self.config(relief=tk.SUNKEN, bg=self.selected_bg, bd=4)
        else:
            self.config(relief=tk.RAISED, bg=self.default_bg, bd=2)
    
    def reset(self):
        """選択状態をリセット"""
        self.selected = False
        self.config(relief=tk.RAISED, bg=self.default_bg, bd=2)


class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ポケモンタイプ対戦分析ツール")
        self.root.geometry("1100x750")
        self.root.configure(bg='#f0f0f0')
        
        self.recommender = PokemonTypeRecommender()
        self.enemy_type_buttons = []
        self.enemy_move_buttons = []
        
        self.create_widgets()
    
    def create_widgets(self):
        # メインコンテナ
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 左側：入力エリア
        left_frame = tk.Frame(main_container, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # タイトル
        title_label = tk.Label(
            left_frame,
            text="🎮 ポケモンタイプ対戦分析",
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
            text="⚔️ 分析する",
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
            text="🔄 リセット",
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
            text="📊 分析結果",
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
        self.result_text.tag_config("highlight", background='#fff9c4')
        
        # 初期メッセージ
        self.show_initial_message()
    
    def create_enemy_type_section(self, parent):
        """敵のタイプ選択セクション"""
        section_frame = tk.LabelFrame(
            parent,
            text="🎯 敵のポケモンタイプ（1〜2個選択）",
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
            row = i // 6
            col = i % 6
            
            btn = TypeButton(
                grid_frame,
                type_name,
                self.recommender.type_colors[type_name],
                lambda t=type_name: self.toggle_enemy_type(t)
            )
            btn.grid(row=row, column=col, padx=3, pady=3)
            self.enemy_type_buttons.append(btn)
    
    def create_enemy_move_section(self, parent):
        """敵の技タイプ選択セクション"""
        section_frame = tk.LabelFrame(
            parent,
            text="⚡ 敵の技タイプ（1〜4個選択）",
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
            row = i // 6
            col = i % 6
            
            btn = TypeButton(
                grid_frame,
                type_name,
                self.recommender.type_colors[type_name],
                lambda t=type_name: self.toggle_enemy_move(t)
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
        self.result_text.insert(tk.END, "　　敵のタイプと技を選択して\n", "title")
        self.result_text.insert(tk.END, "　　「分析する」ボタンを押してください\n\n", "title")
        self.result_text.insert(tk.END, "　　💡 ヒント：\n", "section")
        self.result_text.insert(tk.END, "　　• 敵のタイプは1〜2個選択可能\n")
        self.result_text.insert(tk.END, "　　• 敵の技は1〜4個選択可能\n")
        self.result_text.insert(tk.END, "　　• ボタンをクリックして選択/解除\n")
    
    def analyze(self):
        """分析を実行"""
        # 選択されたタイプを取得
        enemy_types = [b.type_name for b in self.enemy_type_buttons if b.selected]
        enemy_move_types = [b.type_name for b in self.enemy_move_buttons if b.selected]
        
        if not enemy_types:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n\n")
            self.result_text.insert(tk.END, "⚠️ 敵のタイプを選択してください\n", "section")
            return
        
        if not enemy_move_types:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n\n")
            self.result_text.insert(tk.END, "⚠️ 敵の技タイプを選択してください\n", "section")
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
        self.result_text.insert(tk.END, "　✨ おすすめの戦略\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        self.result_text.insert(tk.END, "🎯 おすすめポケモンタイプ\n", "recommend")
        if result["recommended_pokemon_types"]:
            self.result_text.insert(tk.END, f"　{', '.join(result['recommended_pokemon_types'])}\n", "highlight")
            self.result_text.insert(tk.END, "　→ 敵の技を受けにくく安全です\n\n")
        else:
            self.result_text.insert(tk.END, "　該当なし\n")
            self.result_text.insert(tk.END, "　→ 防御面で完全に有利なタイプはありません\n\n")
        
        self.result_text.insert(tk.END, "⚔️ おすすめ技タイプ\n", "recommend")
        if result["recommended_move_types"]:
            self.result_text.insert(tk.END, f"　{', '.join(result['recommended_move_types'])}\n", "highlight")
            self.result_text.insert(tk.END, "　→ 敵に効果的なダメージを与えられます\n\n")
        else:
            self.result_text.insert(tk.END, "　該当なし\n\n")
        
        # 敵情報
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, "　敵の情報\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        self.result_text.insert(tk.END, f"タイプ： {' / '.join(enemy_types)}\n", "section")
        self.result_text.insert(tk.END, f"技　　： {', '.join(enemy_move_types)}\n\n", "section")
        
        # 攻撃効果
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, "　⚔️ 敵に与えるダメージ\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        
        attack_eff = result["attack_effectiveness"]
        
        if attack_eff[4.0]:
            self.result_text.insert(tk.END, "🔥 4倍ダメージ！\n", "damage4x")
            self.result_text.insert(tk.END, f"　{', '.join(attack_eff[4.0])}\n\n", "damage4x")
        
        if attack_eff[2.0]:
            self.result_text.insert(tk.END, "⚡ 2倍ダメージ（効果抜群）\n", "damage2x")
            self.result_text.insert(tk.END, f"　{', '.join(attack_eff[2.0])}\n\n", "damage2x")
        
        if attack_eff[1.0]:
            self.result_text.insert(tk.END, "➖ 等倍ダメージ\n", "damage1x")
            self.result_text.insert(tk.END, f"　{', '.join(attack_eff[1.0])}\n\n", "damage1x")
        
        if attack_eff[0.5]:
            self.result_text.insert(tk.END, "💧 0.5倍（いまいち）\n", "damage05x")
            self.result_text.insert(tk.END, f"　{', '.join(attack_eff[0.5])}\n\n", "damage05x")
        
        if attack_eff[0.25]:
            self.result_text.insert(tk.END, "💧 0.25倍（とても いまいち）\n", "damage05x")
            self.result_text.insert(tk.END, f"　{', '.join(attack_eff[0.25])}\n\n", "damage05x")
        
        if attack_eff[0.0]:
            self.result_text.insert(tk.END, "🚫 無効（ダメージなし）\n", "damage0x")
            self.result_text.insert(tk.END, f"　{', '.join(attack_eff[0.0])}\n\n", "damage0x")
        
        # 防御効果
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n", "title")
        self.result_text.insert(tk.END, "　🛡️ 敵の技から受けるダメージ\n", "title")
        self.result_text.insert(tk.END, "━━━━━━━━━━━━━━━━━━━━\n\n", "title")
        
        defense_ana = result["defense_analysis"]
        
        if defense_ana["無効"]:
            self.result_text.insert(tk.END, "🚫 無効（ダメージ0倍）\n", "damage0x")
            self.result_text.insert(tk.END, f"　{', '.join(defense_ana['無効'])}\n\n", "damage0x")
        
        if defense_ana["いまいち"]:
            self.result_text.insert(tk.END, "🛡️ いまいち（0.5倍以下）\n", "damage05x")
            self.result_text.insert(tk.END, f"　{', '.join(defense_ana['いまいち'])}\n\n", "damage05x")
        
        if defense_ana["有効"]:
            self.result_text.insert(tk.END, "➖ 等倍\n", "damage1x")
            self.result_text.insert(tk.END, f"　{', '.join(defense_ana['有効'])}\n\n", "damage1x")
        
        if defense_ana["ばつぐん"]:
            self.result_text.insert(tk.END, "⚠️ ばつぐん（2倍以上）\n", "damage2x")
            self.result_text.insert(tk.END, f"　{', '.join(defense_ana['ばつぐん'])}\n\n", "damage2x")

if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()