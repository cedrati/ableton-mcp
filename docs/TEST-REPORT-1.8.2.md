# Rapport de test — Remote Script 1.8.2 (fork `cedrati/ableton-mcp`)

- **Date :** 2026-11-19
- **Branche testée :** `feat/mixer-scenes` @ `8d77407`
- **Environnement :** Ableton Live 12 (master nommé « Main »), set de 4 pistes, 2 retours (A-Reverb, …), 8 scènes
- **Méthode :** appels réels via le serveur MCP sur une piste `MCP-TEST` et une scène `MCP-TEST-SCENE` créées pour l'occasion, puis supprimées. Le set utilisateur a été remis dans son état initial (4 pistes, 8 scènes, tête de lecture à 0, master à 0 dB).

## 1. Installation et version

| Vérification | Résultat |
|---|---|
| `get_remote_script_info` : `script_version` = `expected_version` = 1.8.2, `up_to_date: true` | ✅ |
| Script installé dans `~/Music/Ableton/User Library/Remote Scripts/AbletonMCP/` identique à `AbletonMCP_Remote_Script/__init__.py` | ✅ |
| Copie embarquée `MCP_Server/bundled_ableton_remote_script/AbletonMCP_init.py` identique | ✅ |
| Tests unitaires (`uv run --with pytest pytest`) | ✅ 65 passés |

## 2. Nouveaux outils (1.8.0)

### Mixer

| Outil | Test | Résultat |
|---|---|---|
| `set_track_volume` | piste test → 0.6 | ✅ `-10.0 dB`, relu par `get_track_info` |
| `set_track_volume` (`track_type="master"`) | master → 0.85 | ✅ `0.0 dB`, nom `Main` |
| `set_track_panning` | → -0.5 | ✅ `25L` |
| `set_track_send` | send 0 → 0.4 | ✅ `A-Reverb`, `-24.0 dB` |
| `set_track_mute` | piste test on | ✅ |
| `set_track_mute` (`track_type="return"`) | retour 0 on puis off | ✅ (`A-Reverb`) |
| `set_track_solo` | on puis off | ✅ |
| `set_track_arm` | on puis off | ✅ |

### Pistes

| Outil | Test | Résultat |
|---|---|---|
| `duplicate_track` | duplique la piste test (clips + Operator) | ✅ copie à l'index 5 avec réglages mixer, 2 clips et le device |
| `delete_track` | supprime les 2 pistes test | ✅ `track_count` revient à 4 |

### Scènes

| Outil | Test | Résultat |
|---|---|---|
| `get_scenes` | liste | ✅ |
| `create_scene` (`index=-1`) | ajout en fin | ✅ index 8 |
| `set_scene_name` | `MCP-TEST-SCENE` | ✅ |
| `duplicate_scene` | duplique la scène 8 | ✅ index 9, clip dupliqué dans le slot 9 |
| `fire_scene` | lance la scène 9 | ✅ transport démarré (`is_playing: true`) |
| `delete_scene` | supprime 9 puis 8 | ✅ `scene_count` revient à 8 |

### Arrangement

| Outil | Test | Résultat |
|---|---|---|
| `delete_arrangement_clip` | 2 clips posés à 0 et 8 → suppression de l'index 0 | ✅ il reste le clip à 8 |

## 3. Correctifs asynchrones (1.8.1)

| Correctif | Test | Résultat |
|---|---|---|
| `set_arrangement_time` renvoie la nouvelle position | → 16 | ✅ « Playhead moved to beat 16.0 » (avant : renvoyait 0.0) |
| `load_instrument_or_effect` liste les nouveaux devices | Operator sur piste vide | ✅ « New devices: Operator » |
| Rechargement du même device détecté | 2ᵉ chargement d'Operator | ✅ message « reload in place » |
| `create_locator` | **non testé** | ⚠️ voir §5 |

## 4. Correctifs 1.8.2

| Correctif | Test | Résultat |
|---|---|---|
| Refus de Live sans préfixe « Communication error » | mute du master | ✅ `Error setting track mute: The master track cannot be muted` |
| | volume piste 99 | ✅ `Track index out of range` |
| | `fire_scene(42)` | ✅ `Scene index out of range (10 scenes)` |
| | `delete_arrangement_clip` index 5 | ✅ `Arrangement clip index out of range (1 clips)` |
| Connexion conservée après un refus | appel suivant immédiat | ✅ aucune reconnexion nécessaire |
| Vrai nom du master dans `get_session_info` | | ✅ `"Main"` |

## 5. Points d'attention

- **`create_locator` non testé en live :** aucun outil ne permet de supprimer un locator, le test aurait laissé un repère dans le set. Couvert uniquement par `tests/test_async_live_state.py`. Idée : ajouter un `delete_locator`.
- **Capacités non déclarées :** `get_remote_script_info` ne liste pas certaines commandes pourtant fonctionnelles (`set_track_name`, `set_arrangement_time`, `stop_playback`, `get_browser_items_at_path`, `fire_clip`, `set_tempo`…). La liste `capabilities` est incomplète.
- **Type de device :** `get_track_info` renvoie `"type": "unknown"` pour Operator (on attendrait `instrument`). Mineur, antérieur au fork.
- **Version du package :** `pyproject.toml` est toujours en `1.4.5`, alors que le script est passé de 1.8.0 à 1.8.2.

## 6. État GitHub (`cedrati/ableton-mcp`)

| Branche | Local | GitHub | État |
|---|---|---|---|
| `feat/mixer-scenes` | `8d77407` | `8d77407` | ✅ à jour, arbre de travail propre |
| `main` (branche par défaut) | `6f7b801` | `6f7b801` | ⚠️ **ne contient pas `8d77407` (1.8.2)**, elle s'arrête en 1.8.1 + docs |
| `fix/async-live-state` | `eaf52de` | absente | branche locale seulement, déjà incluse dans `feat/mixer-scenes` |

Aucune PR ouverte, ni sur le fork ni vers `ahujasid/ableton-mcp`.

Conséquence : quelqu'un qui installe depuis la branche par défaut du fork récupère le script **1.8.1**, sans les correctifs 1.8.2.

Note : la branche locale `main` suit `origin/main` (upstream) et non `fork/main`, d'où l'indication « ahead 3 ».
