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

## 8. 戦闘システム（基本設計案）

このセクションでは、ナポレオン戦略ゲームにおける戦闘システムの基本的な設計案を記述します。初期プロトタイプでは簡略化されたモデルを採用し、段階的に詳細化していくことを目指します。

### 8.1. 戦闘の発生条件

- **同一地点での敵対ユニット存在:** 敵対する2つ以上の勢力のユニットが、同一の都市（将来的にはマップ上の特定のタイルや地域）に存在する場合、そのターンの解決フェーズで戦闘が発生します。
- **プレイヤーの攻撃指示:** （将来的には）プレイヤーが自軍ユニットに敵ユニットまたは敵都市への攻撃を指示した場合。

### 8.2. 戦闘のフェーズ（ターン内）

- **単一解決フェーズ:** 現時点では、各ゲームターンの終了時に、戦闘が発生している全ての地点で戦闘解決を一度に行います。複雑な戦術マップや複数ラウンドの戦闘は初期段階では導入しません。

### 8.3. 戦闘解決の基本ロジック

戦闘は以下のステップで抽象的に解決されます。

1.  **参加ユニットの特定:** 戦闘が発生する地点に存在する、敵対関係にある全ユニットをリストアップします。
2.  **各ユニットの戦闘力計算:**
    *   **基本攻撃力:** 兵科ごとの基本攻撃値。
    *   **基本防御力:** 兵科ごとの基本防御値。
    *   **兵士数補正:** 兵士数が多いほど戦闘力にプラスの影響（単純な比例ではない可能性も考慮）。
    *   **将軍補正:** 指揮官がいる場合、その将軍の統率・攻撃・防御スキルに応じてユニットの攻撃力・防御力に補正。
    *   **地形補正:** 都市での戦闘の場合、防衛側に防御ボーナス。
    *   （将来的には士気、経験値、補給状態による補正も追加）
3.  **損害計算:**
    *   各ユニットが敵ユニット全体または特定の敵ユニットに対して攻撃を行います。
    *   攻撃側の総攻撃力と防御側の総防御力を比較し、乱数要素も加えて損害兵士数を決定するシンプルな計算式を用います。（例： `損害 = (攻撃側戦闘力 / 防御側戦闘力) * 基本損害定数 * 乱数` ）
    *   防御側は兵士数に応じて損害を吸収します。
4.  **兵士数の更新とユニット除去:**
    *   各ユニットは受けた損害に応じて兵士数が減少します。
    *   兵士数が0以下になったユニットは戦闘から除去（壊滅）されます。

### 8.4. 勝敗判定

-   **殲滅:** 一方の勢力の参加ユニットが全て除去された場合、もう一方の勢力の勝利となります。
-   （将来的には士気崩壊による撤退や、特定ターン数経過後の状況による判定も考慮）

### 8.5. 戦闘結果の反映

-   **兵士数の更新:** 戦闘に参加した全ユニットの兵士数が更新されます。
-   **ユニットの除去:** 壊滅したユニットはゲームから取り除かれます。
-   **都市の占領:** 防衛側ユニットが全滅し、攻撃側ユニットが残存している場合、戦闘発生地点が都市であれば、その都市の支配権が攻撃側の勢力に移ります。

### 8.6. 影響要素（再掲と初期詳細）

-   **兵士数:** ユニットの耐久力であり、戦闘力にも影響。
-   **兵科の基本値:** 各兵科（例: 歩兵、騎兵、砲兵）に固有の攻撃力、防御力、移動力などを設定（`UnitType`マスターデータで管理）。
-   **将軍のスキル:** `General`クラスの`command`, `attack_skill`, `defense_skill`などがユニットの戦闘効率にボーナスを与える。
-   **地形効果:**
    *   **都市:** 防衛側に防御力ボーナス（例: +25%）。
    *   （将来的には平野、森林、山岳なども考慮）
-   **士気 (Morale):** （将来実装）戦闘継続意思。低いと攻撃効率低下、自動撤退など。
-   **補給 (Supply):** （将来実装）補給切れユニットは戦闘力低下、兵士数減少など。
-   **兵科相性:** （将来実装）特定の兵科が他の兵科に対して有利/不利（例: 騎兵 vs 砲兵、方陣歩兵 vs 騎兵）。

### 8.7. 戦闘関連データ (`Battle` オブジェクトの再考)

既存の `DESIGN_DOC.md` セクション7で定義されている `Battle` オブジェクトは、より詳細な戦闘ログやインスタンスベースの戦闘情報を記録する用途で有用です。今回のターンベースの抽象的戦闘解決では、戦闘発生の都度、必要な情報を計算し、結果を直接 `GameState` に反映させる形を初期案とします。必要に応じて、一時的な戦闘状況オブジェクトを生成することも考えられます。

---

このドキュメントは、基本的な枠組みを示すものです。各項目はさらに詳細化されたり、ゲームの具体的なメカニクスに応じて追加・変更されることがあります。
