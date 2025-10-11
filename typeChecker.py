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
            "ばつぐん(2倍以上)": set(),
            "有効(1倍)": set(),
            "いまいち(0.5倍以下)": set(),
            "無効(0倍)": set()
        }
        
        for defend_type in self.types:
            max_damage = 0.0
            min_damage = float('inf')
            has_immunity = False
            
            for move_type in enemy_move_types:
                damage = self.get_attack_effectiveness(move_type, [defend_type])
                if damage == 0:
                    has_immunity = True
                max_damage = max(max_damage, damage)
                min_damage = min(min_damage, damage) if damage > 0 else min_damage
            
            if has_immunity:
                defense_analysis["無効(0倍)"].add(defend_type)
            elif max_damage >= 2.0:
                defense_analysis["ばつぐん(2倍以上)"].add(defend_type)
            elif max_damage <= 0.5:
                defense_analysis["いまいち(0.5倍以下)"].add(defend_type)
            else:
                defense_analysis["有効(1倍)"].add(defend_type)
        
        # セットをリストに変換
        return {k: list(v) for k, v in defense_analysis.items()}
    
    def recommend_pokemon(self, enemy_types: List[str], enemy_move_types: List[str]) -> Dict:
        """最適なポケモンタイプと技タイプを推奨"""
        attack_effectiveness = self.analyze_enemy(enemy_types)
        defense_analysis = self.analyze_defense(enemy_move_types)
        
        # 攻撃面で有利なタイプ（4倍または2倍）
        good_attack_types = set(attack_effectiveness[4.0] + attack_effectiveness[2.0])
        
        # 防御面で有利なタイプ（いまいちまたは無効）
        good_defense_types = set(defense_analysis["いまいち(0.5倍以下)"] + defense_analysis["無効(0倍)"])
        
        # 防御面で不利なタイプを除外
        bad_defense_types = set(defense_analysis["ばつぐん(2倍以上)"])
        
        # 推奨ポケモンタイプ（防御面で有利で、攻撃面で不利でない）
        recommended_pokemon_types = good_defense_types - bad_defense_types
        
        # 推奨技タイプ（攻撃面で有利）
        recommended_move_types = good_attack_types
        
        return {
            "attack_effectiveness": attack_effectiveness,
            "defense_analysis": defense_analysis,
            "recommended_pokemon_types": list(recommended_pokemon_types),
            "recommended_move_types": list(recommended_move_types)
        }


class PokemonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ポケモンタイプ推奨アプリ")
        self.root.geometry("750x700")
        
        self.recommender = PokemonTypeRecommender()
        
        self.create_widgets()
    
    def create_widgets(self):
        # メインフレーム
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 敵のタイプ選択
        ttk.Label(main_frame, text="敵のタイプを選択:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        enemy_type_frame = ttk.Frame(main_frame)
        enemy_type_frame.grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.enemy_type1_var = tk.StringVar()
        self.enemy_type2_var = tk.StringVar(value="なし")
        
        ttk.Label(enemy_type_frame, text="タイプ1:").grid(row=0, column=0, padx=5)
        enemy_type1_combo = ttk.Combobox(enemy_type_frame, textvariable=self.enemy_type1_var, 
                                         values=self.recommender.types, state='readonly', width=12)
        enemy_type1_combo.grid(row=0, column=1, padx=5)
        enemy_type1_combo.current(0)
        
        ttk.Label(enemy_type_frame, text="タイプ2:").grid(row=0, column=2, padx=5)
        enemy_type2_combo = ttk.Combobox(enemy_type_frame, textvariable=self.enemy_type2_var,
                                         values=["なし"] + self.recommender.types, state='readonly', width=12)
        enemy_type2_combo.grid(row=0, column=3, padx=5)
        enemy_type2_combo.current(0)
        
        # 敵の技タイプ選択
        ttk.Label(main_frame, text="敵の技のタイプを選択:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        
        move_type_frame = ttk.Frame(main_frame)
        move_type_frame.grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.enemy_move1_var = tk.StringVar()
        self.enemy_move2_var = tk.StringVar(value="なし")
        self.enemy_move3_var = tk.StringVar(value="なし")
        self.enemy_move4_var = tk.StringVar(value="なし")
        
        for i, var in enumerate([self.enemy_move1_var, self.enemy_move2_var, 
                                  self.enemy_move3_var, self.enemy_move4_var]):
            ttk.Label(move_type_frame, text=f"技{i+1}:").grid(row=i//2, column=(i%2)*2, padx=5, pady=2)
            combo = ttk.Combobox(move_type_frame, textvariable=var,
                                values=["なし"] + self.recommender.types, state='readonly', width=12)
            combo.grid(row=i//2, column=(i%2)*2+1, padx=5, pady=2)
            if i == 0:
                combo.current(1)
            else:
                combo.current(0)
        
        # 分析ボタン
        analyze_button = ttk.Button(main_frame, text="分析する", command=self.analyze)
        analyze_button.grid(row=4, column=0, pady=15)
        
        # 結果表示エリア
        result_frame = ttk.Frame(main_frame)
        result_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # スクロールバー付きテキストエリア
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(result_frame, height=25, width=100, 
                                   yscrollcommand=scrollbar.set, font=('Arial', 10))
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # タグの設定（色付け）
        self.result_text.tag_config("header", font=('Arial', 12, 'bold'), foreground='blue')
        self.result_text.tag_config("subheader", font=('Arial', 11, 'bold'))
        self.result_text.tag_config("recommendation", font=('Arial', 11, 'bold'), foreground='green')
    
    def analyze(self):
        # 入力取得
        enemy_types = [self.enemy_type1_var.get()]
        if self.enemy_type2_var.get() != "なし":
            enemy_types.append(self.enemy_type2_var.get())
        
        enemy_move_types = []
        for var in [self.enemy_move1_var, self.enemy_move2_var, 
                    self.enemy_move3_var, self.enemy_move4_var]:
            if var.get() != "なし":
                enemy_move_types.append(var.get())
        
        if not enemy_move_types:
            enemy_move_types = [self.recommender.types[0]]  # デフォルト
        
        # 分析実行
        result = self.recommender.recommend_pokemon(enemy_types, enemy_move_types)
        
        # 結果表示
        self.result_text.delete(1.0, tk.END)
        
        # 敵情報
        self.result_text.insert(tk.END, "=== 敵の情報 ===\n", "header")
        self.result_text.insert(tk.END, f"タイプ: {' / '.join(enemy_types)}\n")
        self.result_text.insert(tk.END, f"技のタイプ: {', '.join(enemy_move_types)}\n\n")
        
        # 攻撃効果（敵に与えるダメージ）
        self.result_text.insert(tk.END, "=== 敵に与えるダメージ倍率 ===\n", "header")
        attack_eff = result["attack_effectiveness"]
        
        if attack_eff[4.0]:
            self.result_text.insert(tk.END, "【4倍ダメージ】\n", "subheader")
            self.result_text.insert(tk.END, f"  {', '.join(attack_eff[4.0])}\n\n")
        
        if attack_eff[2.0]:
            self.result_text.insert(tk.END, "【2倍ダメージ】\n", "subheader")
            self.result_text.insert(tk.END, f"  {', '.join(attack_eff[2.0])}\n\n")
        
        if attack_eff[1.0]:
            self.result_text.insert(tk.END, "【1倍ダメージ（等倍）】\n", "subheader")
            self.result_text.insert(tk.END, f"  {', '.join(attack_eff[1.0])}\n\n")
        
        if attack_eff[0.5]:
            self.result_text.insert(tk.END, "【0.5倍ダメージ（いまいち）】\n", "subheader")
            self.result_text.insert(tk.END, f"  {', '.join(attack_eff[0.5])}\n\n")
        
        if attack_eff[0.25]:
            self.result_text.insert(tk.END, "【0.25倍ダメージ】\n", "subheader")
            self.result_text.insert(tk.END, f"  {', '.join(attack_eff[0.25])}\n\n")
        
        if attack_eff[0.0]:
            self.result_text.insert(tk.END, "【無効（0倍）】\n", "subheader")
            self.result_text.insert(tk.END, f"  {', '.join(attack_eff[0.0])}\n\n")
        
        # 防御効果（敵の技から受けるダメージ）
        self.result_text.insert(tk.END, "\n=== 敵の技から受けるダメージ ===\n", "header")
        defense_ana = result["defense_analysis"]
        
        for category, types in defense_ana.items():
            if types:
                self.result_text.insert(tk.END, f"【{category}】\n", "subheader")
                self.result_text.insert(tk.END, f"  {', '.join(types)}\n\n")
        
        # 推奨
        self.result_text.insert(tk.END, "\n=== おすすめのポケモンと技 ===\n", "header")
        
        self.result_text.insert(tk.END, "【おすすめポケモンタイプ】\n", "recommendation")
        if result["recommended_pokemon_types"]:
            self.result_text.insert(tk.END, f"  {', '.join(result['recommended_pokemon_types'])}\n")
            self.result_text.insert(tk.END, "  → 敵の技を受けにくく、耐久性があります\n\n")
        else:
            self.result_text.insert(tk.END, "  該当なし（防御面で完全に有利なタイプはありません）\n\n")
        
        self.result_text.insert(tk.END, "【おすすめ技タイプ】\n", "recommendation")
        if result["recommended_move_types"]:
            self.result_text.insert(tk.END, f"  {', '.join(result['recommended_move_types'])}\n")
            self.result_text.insert(tk.END, "  → 敵に効果的なダメージを与えられます\n")
        else:
            self.result_text.insert(tk.END, "  該当なし\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = PokemonApp(root)
    root.mainloop()