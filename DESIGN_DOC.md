# データ構造設計案 (DESIGN_DOC.md)

## はじめに

本文書は、戦略ゲーム「ナポレオン」のコアとなるデータ構造の初期設計案を記述するものです。
「信長の野望」風のゲームシステムを想定し、主要なゲーム要素をプログラム上でどのように表現するかを定義します。
この設計は初期段階のものであり、今後の開発やフィードバックに応じて変更される可能性があります。

## 1. マップデータ

### 1.1. 都市 (City)

各都市が持つ情報を定義します。

- `city_id`: 都市ID (ユニークな識別子, 例: `paris`, `london`)
- `name`: 都市名 (例: "パリ", "ロンドン")
- `region_id`: 所属地域ID (どの地域に属するか)
- `coordinates`: マップ上の座標 (例: `(x, y)`) - GUI表示用
- `type`: 都市タイプ (例: `"capital"`, `"major_city"`, `"fortress"`, `"town"`)
- `population`: 人口 (例: `100000`)
- `max_population`: 最大人口 (例: `500000`)
- `economy`: 経済力 (商業や市場の規模を示す指標, 例: `1200`)
- `industry`: 工業力 (兵器生産や施設建設の基盤, 例: `800`)
- `agriculture`: 農業力 (食糧生産の基盤, 例: `1500`)
- `defense_rating`: 防御度 (城壁や要塞の堅牢さ, 例: `75`)
- `current_owner_faction_id`: 現在の支配勢力ID
- `garrisoned_units`: 駐留部隊リスト (Unit IDのリスト)
- `buildings`: 建設済み施設リスト (例: `["market_lv2", "barracks_lv1"]`)
- `developable_slots`: 開発可能スロット数 (都市の規模に応じて変動)
- `loyalty_to_owner`: 支配勢力への忠誠度/安定度 (例: `80` / 0-100)
- `resource_production`: 生産資源 (例: `{"gold": 100, "food": 200, "production_points": 50}`)

### 1.2. 地域 (Region)

複数の都市をまとめる広域の単位。国境線や文化圏の表現にも利用。

- `region_id`: 地域ID (ユニークな識別子, 例: `ile_de_france`, `greater_london`)
- `name`: 地域名 (例: "イル＝ド＝フランス", "大ロンドン")
- `cities_in_region`: 地域内の都市IDリスト
- `terrain_type`: 主要な地形タイプ (例: `"plains"`, `"forest"`, `"mountain"`) - 戦闘や移動に影響
- `climate`: 気候 (例: `"temperate"`) - 消耗などに影響

### 1.3. マップ全体 (GameMap)
- `map_id`: マップID (例: `europe_1805`)
- `dimensions`: マップのサイズ (例: `(width, height)`)
- `city_list`: マップ上の全都市オブジェクトのリスト
- `region_list`: マップ上の全地域オブジェクトのリスト
- `adjacency_list`: 都市間または地域間の隣接関係 (例: `{ "paris": ["orleans", "reims"] }`)

## 2. ユニットデータ

### 2.1. 将軍 (General)

ナポレオンやウェリントンなど、歴史上の人物。部隊を率いたり、内政や外交を担当。

- `general_id`: 将軍ID (ユニークな識別子, 例: `napoleon`, `wellington`)
- `name`: 名前 (例: "ナポレオン・ボナパルト")
- `portrait_path`: 顔グラフィックのパス
- `faction_id`: 所属勢力ID (初期所属、亡命や登用で変更可能性あり)
- `birth_year`: 登場年/生年
- `death_year`: 死亡年 (設定により変動、または戦死・病死など)
- `loyalty`: 忠誠度 (0-100, 勢力への忠誠)
- `command`: 統率力 (部隊の規模や戦闘効率に影響)
- `attack_skill`: 武勇 (直接戦闘や突撃の効果に影響)
- `defense_skill`: 防御指揮 (防御戦闘時の効果に影響)
- `intelligence`: 知略 (計略の成功率や計略防御、研究速度に影響)
- `politics`: 政務 (内政効率や外交交渉に影響)
- `charisma`: 魅力 (登用成功率、民忠上昇、部隊の士気に影響)
- `experience`: 経験値
- `level`: レベル
- `skills_and_traits`: 特技・特性リスト (例: `["artillery_master", "forced_march", "inspiring_leader"]`)
- `current_location_city_id`: 現在の所在地 (都市ID)
- `status`: 状態 (例: `"active"`, `"wounded"`, `"captured"`, `"standby"`)
- `assigned_corps_id`: 所属軍団ID (もし軍団システムを導入する場合)
- `led_units`: 直接指揮している部隊リスト (Unit IDのリスト) - シンプルな場合は将軍が直接部隊を持つ

### 2.2. 兵科 (UnitType) - マスターデータ

歩兵、騎兵、砲兵などの種類を定義。

- `unit_type_id`: 兵科ID (例: `line_infantry_french`, `cuirassier`, `12lb_foot_artillery`)
- `name`: 兵科名 (例: "フランス戦列歩兵", "胸甲騎兵", "12ポンド野戦砲")
- `description`: 詳細説明
- `icon_path`: ユニットアイコンのパス
- `base_attack`: 基本攻撃力
- `base_defense`: 基本防御力
- `movement_points`: 移動力
- `range`: 射程 (砲兵など)
- `recruitment_cost`: 徴兵コスト (資金、資源など)
- `upkeep_cost`: 維持コスト (資金、食料など)
- `recruitment_time`: 徴兵期間 (ターン数)
- `required_buildings`: 徴兵に必要な施設 (例: `["barracks_lv2"]`)
- `required_technology`: 徴兵に必要な技術 (例: `["improved_muskets"]`)
- `terrain_modifiers`: 地形適性ボーナス/ペナルティ (例: `{"forest": {"attack_mod": -0.1, "defense_mod": 0.2}}`)
- `strong_against_types`: 有利な敵兵科IDリスト
- `weak_against_types`: 不利な敵兵科IDリスト
- `is_ranged`: 遠隔攻撃ユニットか (true/false)
- `can_siege`: 包囲攻撃可能か (true/false)

### 2.3. 個別部隊 (ArmyUnit) - ゲーム中に存在する部隊のインスタンス

実際にマップ上を行軍したり戦闘したりする部隊。

- `unit_id`: 部隊ID (ゲーム内でユニーク)
- `unit_type_id`: 兵科ID (UnitTypeを参照)
- `leading_general_id`: 指揮官ID (Generalを参照、任意だが強力な指揮官はボーナス)
- `owning_faction_id`: 所属勢力ID
- `current_location`: 現在位置 (都市ID、またはマップ座標 `(x,y)`)
- `soldiers`: 現在の兵士数
- `max_soldiers`: 最大兵士数 (兵科や将軍の統率により上限あり)
- `morale`: 士気 (0-100)
- `experience_level`: 練度/経験レベル
- `supply_status`: 補給状態 (例: `"fully_supplied"`, `"low_supply"`, `"out_of_supply"`)
- `formation`: 陣形 (もし戦闘で考慮する場合)
- `status`: 状態 (例: `"idle"`, `"moving"`, `"attacking"`, `"sieging"`, `"garrisoned"`)

## 3. 勢力データ (Faction)

フランス、イギリス、オーストリアなど、プレイヤーまたはAIが操作する国家。

- `faction_id`: 勢力ID (ユニークな識別子, 例: `france_empire`, `great_britain`)
- `name`: 勢力名 (例: "フランス第一帝政", "グレートブリテン及びアイルランド連合王国")
- `short_name`: 短縮名 (例: "フランス", "イギリス")
- `flag_icon_path`: 国旗アイコンのパス
- `leader_general_id`: 現在の指導者 (General ID)
- `heir_general_id`: 後継者 (General ID, 君主制の場合など)
- `government_type`: 政体 (例: `"empire"`, `"monarchy"`, `"republic"`)
- `capital_city_id`: 首都 (City ID)
- `controlled_cities_ids`: 支配下の都市IDリスト
- `controlled_regions_ids`: 支配下の地域IDリスト (都市の支配状況から派生可能)
- `generals_list_ids`: 所属する将軍IDリスト
- `army_units_list_ids`: 保有する部隊IDリスト
- `treasury`: 国庫の資金
- `food_reserves`: 食料備蓄
- `manpower_pool`: 徴兵可能な人的資源
- `stability`: 国内安定度 (0-100)
- `prestige`: 国威・名声
- `diplomatic_relations`: 外交関係リスト (各勢力との関係: `{"target_faction_id": "great_britain", "status": "war", "relation_value": -100, "treaties": []}`)
  - `status`: `"peace"`, `"war"`, `"alliance"`, `"vassal"`, `"trade_agreement"`
  - `treaties`: 有効な条約リスト (例: `["military_alliance_treaty_id_123"]`)
- `research_points`: 研究ポイント
- `current_research_tech_id`: 現在研究中の技術ID
- `researched_technologies_ids`: 研究済み技術IDリスト
- `active_policies_ids`: 施行中の政策IDリスト
- `national_ideas_or_bonuses`: 国家固有のアイデアやボーナス (例: `["elan_vital", "grand_armee_doctrine"]`)
- `victory_points`: 勝利ポイント (特定の勝利条件用)
- `ai_personality_type`: AIの性格タイプ (もしAI勢力なら)

## 4. 技術データ (Technology) - マスターデータ

研究することで新たなユニット、施設、能力をアンロック。

- `technology_id`: 技術ID (例: `corps_system`, `improved_artillery_tactics`)
- `name`: 技術名
- `description`: 技術の説明
- `research_cost`: 研究に必要なコスト (研究ポイントなど)
- `prerequisites_tech_ids`: 前提となる技術IDリスト
- `unlocks`: この技術でアンロックされるもの (ユニットタイプ、建物、政策など)
  - `units`: アンロックされるユニットタイプIDリスト
  - `buildings`: アンロックされる建物IDリスト
  - `policies`: アンロックされる政策IDリスト
  - `abilities`: アンロックされる特殊能力やボーナス

## 5. 政策データ (Policy) - マスターデータ

採用することで国家に様々な効果をもたらす。

- `policy_id`: 政策ID (例: `conscription_act`, `free_trade_agreement`)
- `name`: 政策名
- `description`: 政策の説明
- `enactment_cost`: 採用コスト (資金、政治力など)
- `upkeep_cost`: 維持コスト (毎ターン)
- `effects`: 政策の効果リスト (例: `[{"type": "manpower_recovery_bonus", "value": 0.1}, {"type": "trade_efficiency_bonus", "value": 0.05}]`)
- `prerequisites_tech_ids`: 前提技術IDリスト
- `conflicting_policies_ids`: 同時に採用できない対立政策IDリスト

## 6. ゲーム進行データ (GameState)

ゲーム全体の現在の状態を管理。

- `current_turn`: 現在のターン数
- `current_season_or_month`: 現在の季節または月 (ターン進行の単位)
- `active_faction_id`: 現在行動中の勢力ID (ターン制の場合)
- `game_speed`: ゲーム速度
- `active_historical_events`: 発生中の歴史イベントリスト
- `global_flags`: グローバル変数・フラグ (特定のイベント発生条件など)
- `world_tension`: 世界の緊張度 (外交やイベントに影響)
- `player_faction_id`: プレイヤーが操作している勢力ID

## 7. 戦闘データ (Battle) - 戦闘発生時に動的に生成

- `battle_id`: 戦闘ID
- `attacking_faction_id`: 攻撃側勢力ID
- `defending_faction_id`: 防御側勢力ID
- `attacking_units_ids`: 攻撃側参加ユニットIDリスト
- `defending_units_ids`: 防御側参加ユニットIDリスト
- `location_city_id_or_coords`: 戦闘発生場所 (都市IDまたは座標)
- `terrain_at_battle`: 戦闘地の地形
- `weather_at_battle`: 戦闘時の天候
- `battle_phase`: 戦闘フェイズ (例: `"skirmish"`, `"main_engagement"`, `"rout"`)
- `attacker_casualties`: 攻撃側損害
- `defender_casualties`: 防御側損害
- `outcome`: 戦闘結果 (例: `"attacker_victory"`, `"defender_victory"`, `"stalemate"`)

---

このドキュメントは、基本的な枠組みを示すものです。各項目はさらに詳細化されたり、ゲームの具体的なメカニクスに応じて追加・変更されることがあります。
