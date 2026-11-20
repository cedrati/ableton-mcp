<div align="center">

# Ableton MCP — Extended Edition

**Let Claude (or any MCP client) compose, arrange, mix, listen to and analyse music in Ableton Live.**

An extended version of [ableton-mcp](https://github.com/ahujasid/ableton-mcp) by **Olivier Cedrati** ([@cedrati](https://github.com/cedrati)).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Remote Script](https://img.shields.io/badge/Remote%20Script-1.15.0-blue)
![Live](https://img.shields.io/badge/Ableton%20Live-11%20%7C%2012-black)
![Tests](https://img.shields.io/badge/tests-245%20passing-brightgreen)

[Quickstart](#quickstart) · [What's new](#what-this-edition-adds) · [Tools](#tool-reference) · [Changelog](CHANGELOG.md) · [Issues](https://github.com/cedrati/ableton-mcp/issues)

</div>

---

## About

[Ableton MCP](https://github.com/ahujasid/ableton-mcp), created by Siddharth Ahuja, connects Ableton Live to AI assistants through the [Model Context Protocol](https://modelcontextprotocol.io): the assistant can create tracks and clips, write notes, load devices and drive the transport.

**This edition, written and maintained by Olivier Cedrati, turns it into a full production assistant.** Beyond writing notes, the assistant can mix (faders, sends, return and main-track effects, routing), **listen** to the result and judge it like a mastering engineer (LUFS, true peak, tonal balance, stereo, a spectrogram it can look at), and compose with real music-theory knowledge (scales and modes, style sheets, key and chord analysis, clip transformations, voice-led progressions).

It is developed on the `feat/mixer-scenes` branch of [cedrati/ableton-mcp](https://github.com/cedrati/ableton-mcp). The `ableton-mcp` package on PyPI is the **original** project and does not include any of this — install from this repository as shown below.

## What this edition adds

| Area | What the assistant can do |
|---|---|
| **Mixing** | Volume, pan, sends, mute, solo, arm on tracks, return tracks and the main track. Load effects on return tracks and the main track (a shared reverb, a limiter). Read every parameter as Live displays it (`Bell`, `1.56 kHz`, `-6.0 dB`). |
| **Routing** | Set track inputs, outputs and monitoring: layer one MIDI part on several instruments, resample the main output, route to a return. |
| **Listening & mastering analysis** | Record the main output in real time and get a report: loudness per ITU-R BS.1770 / EBU R128 (integrated, short-term, momentary, loudness range), true peak, PLR, tonal balance against a reference curve, resonances, stereo width per band, low-end mono, each track's meter level, a spectrogram image — and ranked findings with fixes for a delivery target (streaming, club, classical, broadcast, podcast). |
| **Drums** | Program a Drum Rack from 19 electronic patterns (techno, house, garage, breaks, d'n'b...) or your own step grids: pads found by name, Euclidean and polyrhythmic layers, ratchets, ghost notes, per-note probability, fills, swing, Live's Groove Pool. |
| **Music theory** | ~50 scales and modes with their character and typical styles; 24 style sheets (baroque to techno); key, mode and chord analysis of a clip with roman numerals; 17 clip transformations (mode change, diatonic transposition, harmonization, arpeggios, voicings, swing...); voice-led chord progressions; Live 12's song scale. |
| **Clips** | Notes in Arrangement clips, partial note removal, loop brace and markers, warp (modes, markers, conform a loop to the tempo), clip automation envelopes. |
| **Files** | Import Standard MIDI Files into clips; analyse any WAV/AIFF. |
| **Session** | Duplicate and delete tracks; list, create, rename, duplicate, launch and delete scenes; delete Arrangement clips. |
| **Devices & browser** | Plugins (VST, VST3, AU), User Library and Packs are browsable and loadable like built-in devices. |
| **Reliability** | Playhead moves, locator creation and device loading reply only once Live has applied them; version handshake between server and Remote Script; capability checks so a newer server never sends a command an older script would misread. |

Everything is covered by automated tests (245) and checked end to end in Ableton Live 12. See the [Changelog](CHANGELOG.md) for the details of each release.

---

## Quickstart

### Requirements

- **Ableton Live 11 or 12** (Live 12 for the song scale; Live 10 works for the original features)
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** — on macOS: `brew install uv`
- An MCP client: Claude Code, Claude Desktop, Cursor...

Python (3.10+) and the dependencies, including `numpy`, are installed automatically by `uv`.

### 1. Add the server to your MCP client

<details open>
<summary><b>Claude Code</b></summary>

```bash
claude mcp add ableton -s user -- uvx --from git+https://github.com/cedrati/ableton-mcp@feat/mixer-scenes ableton-mcp
```
</details>

<details>
<summary><b>Claude Desktop</b> — Settings → Developer → Edit Config</summary>

```json
{
  "mcpServers": {
    "AbletonMCP": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/cedrati/ableton-mcp@feat/mixer-scenes", "ableton-mcp"]
    }
  }
}
```
</details>

<details>
<summary><b>Cursor</b> — Settings → MCP, as a command</summary>

```
uvx --from git+https://github.com/cedrati/ableton-mcp@feat/mixer-scenes ableton-mcp
```
</details>

Run the server in **one** client at a time.

### 2. Install the Remote Script into Live

```bash
uvx --from git+https://github.com/cedrati/ableton-mcp@feat/mixer-scenes ableton-mcp-install-script
```

This copies the script into your User Library's `Remote Scripts/AbletonMCP` folder (found from Live's own settings; `--list-targets` shows where it would go, `--target <folder>` forces a location). A previous version is kept as `__init__.py.bak`.

The server and the Remote Script must come from the **same version** — always install both from this repository.

### 3. Enable it in Live

1. Start (or **restart**) Ableton Live.
2. **Settings → Link, Tempo & MIDI → Control Surface:** choose **AbletonMCP**, with Input and Output set to **None**.

### 4. Check

Ask the assistant to run `get_remote_script_info`. It should report `script_version` **1.15.0** and `up_to_date: true`.

### Updating

1. Re-run the install command of step 2.
2. **Restart Live** — re-selecting the control surface does not reload the code.
3. Restart your MCP client. If it still runs old code: `uv cache clean ableton-mcp` (with the client closed).

---

## What you can ask

**Compose and arrange**
- *"Write a C minor organ fugue: subject, answer at the fifth, countersubject, stretto."*
- *"Give me a deep house progression in A minor with offbeat stabs, then a rolling bassline."*
- *"Analyse the clip on track 2: key, chords, roman numerals."*
- *"Re-harmonise this melody in Dorian, add a third above, swing it at 58 %."*
- *"Import this MIDI file and transpose it to F#."*
- *"Program 8 bars of rolling techno on the 909 kit, with a 5-in-16 percussion layer and a clap roll every 4 bars."*

**Mix and master**
- *"Listen to the whole track and tell me if it's ready for streaming."*
- *"Put a cathedral reverb on return A and send the pads to it."*
- *"The low end is muddy — find out why and fix it."*
- *"Layer the bass MIDI on a second synth one octave down."*

---

## Tool reference

Indexes start at 0. Times and lengths are in **beats**. Notes use MIDI numbers (60 = C4 in scientific pitch, shown as C3 in Live).

### Session and transport

| Tool | Description |
|---|---|
| `get_session_info` / `get_session_snapshot` | Tempo, time signature, tracks, transport; full state dump. |
| `set_tempo` · `start_playback` · `stop_playback` | Transport. |
| `get_scenes` · `create_scene` · `set_scene_name` · `duplicate_scene` · `fire_scene` · `delete_scene` | Scenes. |
| `switch_to_arrangement_view` · `set_arrangement_time` · `create_locator` | Arrangement view, playhead, locators. |
| `get_remote_script_info` | Version handshake and capabilities. |

### Tracks, mixer and routing

| Tool | Description |
|---|---|
| `create_midi_track` · `create_audio_track` · `set_track_name` · `duplicate_track` · `delete_track` | Tracks. |
| `get_track_info` | Track, return track (`track_type="return"`) or main track (`"master"`): mixer state, clip slots, devices. |
| `set_track_volume` · `set_track_panning` · `set_track_send` · `set_track_mute` · `set_track_solo` · `set_track_arm` | Mixer; reply with Live's display value (`-6.0 dB`, `25L`). `track_type` reaches return tracks and the main track. |
| `get_track_routing` · `set_track_routing` | Input/output type and channel, monitoring (`in`, `auto`, `off`), matched by the names Live shows. |
| `get_track_meters` | Live's output meter of every track, return and the main track. |

### Devices and browser

| Tool | Description |
|---|---|
| `get_browser_tree` · `get_browser_items_at_path` | Browse `instruments`, `sounds`, `drums`, `audio_effects`, `midi_effects`, `plugins`, `user_library`, `packs`, `samples`, `max_for_live`, `current_project`. |
| `load_instrument_or_effect` · `load_drum_kit` | Load by browser URI, on a track, a return track or the main track. |
| `get_device_parameters` · `set_device_parameter` | Every parameter with its range, Live's display string and, for list parameters, the names of the values. |

### Clips and notes

| Tool | Description |
|---|---|
| `create_clip` · `create_audio_clip` · `set_clip_name` · `fire_clip` · `stop_clip` · `delete_clip` | Session clips. |
| `get_clip_notes` · `add_notes_to_clip` · `clear_notes_from_clip` · `remove_notes` | Notes, in Session or Arrangement clips (`location="arrangement"`); `remove_notes` clears a time/pitch range only. |
| `get_clip_loop` · `set_clip_loop` | Loop switch, loop brace, start/end markers. |
| `get_clip_warp` · `set_clip_warp` · `edit_warp_markers` | Warp mode, markers, pitch, gain; `original_bpm` conforms a loop to the tempo. |
| `get_clip_automation` · `set_clip_automation` | Clip envelopes for device and mixer parameters (Session clips). |
| `get_arrangement_clips` · `duplicate_to_arrangement` · `set_arrangement_clip_name` · `delete_arrangement_clip` | Arrangement clips. |
| `import_midi_file` | Import a `.mid` file (track/channel filters, transposition) or describe it. |

### Listening and analysis

| Tool | Description |
|---|---|
| `listen_to_arrangement` | Records the main output between two song positions on a temporary track (in real time), samples every track's meter, then returns the mix report and the spectrogram image. The track is removed afterwards; the take stays in the project's `Samples/Recorded` folder. |
| `analyze_mix` | The same mastering report for any WAV/AIFF file. |
| `analyze_audio_file` | Lightweight level report (no `numpy` needed). |
| `record_arrangement` · `get_recording_status` · `stop_arrangement_recording` · `get_audio_clip_file` | Record armed tracks into the Arrangement between two positions; find the recorded file. |

The mix report checks: integrated / short-term / momentary loudness and loudness range (validated on EBU reference signals), true peak (4× oversampled), PLR and crest factor, long-term spectrum and its tilt against a −4.5 dB/octave reference (sub, lows, low-mids, mids, high-mids, highs, air), narrow peaks with their note names, stereo correlation and width per band, low-end mono, DC offset. Each finding comes with a severity and a concrete fix using Live's own devices.

### Drums and groove

| Tool | Description |
|---|---|
| `drum_patterns` | Pattern library (techno four, rolling, hypnotic, minimal, dub, hard, acid, Detroit, house, deep house, tech house, afro house, UK garage, breakbeat, electro, drum & bass, dubstep, trap, EBM) with tempo, swing and production notes; Euclidean rhythms. |
| `get_drum_map` | A track's Drum Rack pads and the role each plays (kick, clap, hats, perc...). |
| `write_drum_pattern` | Program a clip from a style and/or grids per role: `x` hit, `X` accent, `o` ghost, `2`-`4` ratchet, `?`/`*` probability; Euclidean layers, swing, fills, variation, humanize. |
| `get_groove_pool` · `set_clip_groove` · `set_groove_params` | Live's Groove Pool: list grooves, apply one to a clip, adjust amounts and the global Groove amount. |

### Music theory and composition

| Tool | Description |
|---|---|
| `music_scales` | ~50 scales and modes — church modes, harmonic/melodic minor families, pentatonics, blues, bebop, symmetric, Japanese, gamelan, flamenco — with character, characteristic note, styles; or one scale in a key: spelled notes, diatonic chords with roman numerals and functions, relative modes, Live's name. |
| `music_styles` | 24 style sheets (baroque, classical, jazz, bossa nova, blues, gospel/neo-soul, funk, pop, rock, house, techno, trance, drum & bass, boom bap, lo-fi, trap, R&B, reggae, reggaeton, afrobeat, flamenco, film score, ambient, synthwave): tempo, metre, scales, harmony, progressions, groove and swing, bass, melody, arrangement, Live devices. |
| `music_chord_ideas` | Reharmonisation ideas for a chord, with the reason for each. |
| `analyze_clip_music` | Key and mode, chords with roman numerals (`basic` or `jazz` vocabulary), out-of-scale notes, range, rhythm, melodic motion. |
| `transform_clip` | Chain of operations, in place or into an empty slot: `transpose`, `transpose_diatonic`, `change_mode`, `snap_to_scale`, `invert`, `retrograde`, `time_scale`, `quantize`, `swing`, `humanize`, `accent`, `articulate`, `fold_range`, `harmonize`, `arpeggiate`, `strum`, `voice_chords`. |
| `write_progression` | Roman numerals (secondary dominants, borrowed chords, Neapolitan) or a style's progression, voice-led, played with an accompaniment pattern and a bass line. |
| `get_song_scale` · `set_song_scale` | Live 12's song scale and Scale Mode. |

### Good to know

- **Live's API has limits.** A script cannot save the set, export audio, create group tracks, or write Arrangement (song-level) automation such as tempo changes. Live's own analysers (Spectrum, EQ Eight's display, Max for Live meters) don't expose their readings — which is why listening works by recording the main output.
- **Listening takes real time:** analysing a 3-minute song means playing it for 3 minutes.
- **Device loading, playhead moves and locators** reply only once Live has applied them. Loading the same device that is already on a track resets it in place (the reply says so).
- **Destructive tools** (`delete_track`, `delete_scene`, `delete_clip`, `delete_arrangement_clip`) do what they say — save your set before big experiments.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `up_to_date: false`, or "missing capability" errors | The script in Live is older than the server. Re-run the install command, then **restart Live**. |
| The server still runs old code after an update | Restart the MCP client; if needed `uv cache clean ableton-mcp` with the client closed. |
| No connection | Check that **AbletonMCP** is selected as a Control Surface and that only one MCP client runs the server. |
| Timeouts on big requests | Ask for the work in smaller steps. |

---

## How it works

```
MCP client (Claude…)  ⇄  MCP server (MCP_Server/, Python)  ⇄  TCP 127.0.0.1:9877  ⇄  Remote Script inside Live (AbletonMCP_Remote_Script/)
```

- The **Remote Script** runs inside Live and executes commands through Live's Python API. It listens on localhost only (set `ABLETON_MCP_HOST` deliberately to change that).
- The **MCP server** exposes the tools, checks the script's version and capabilities, and does the heavy work outside Live: audio analysis, MIDI files, music theory.
- Messages are JSON objects: `{"type": ..., "params": ...}` → `{"status": ..., "result" | "message": ...}`.

### Development

```bash
git clone -b feat/mixer-scenes https://github.com/cedrati/ableton-mcp
cd ableton-mcp
uv run --with pytest pytest -q          # 245 tests, no Live needed
uv run ableton-mcp-install-script       # install your working copy into Live
```

When you change the Remote Script, bump `SCRIPT_VERSION` (and `EXPECTED_REMOTE_SCRIPT_VERSION` in `MCP_Server/remote_script_install.py`), copy it to `MCP_Server/bundled_ableton_remote_script/AbletonMCP_init.py`, and add an entry to the [Changelog](CHANGELOG.md).

---

## Privacy

The original project includes optional telemetry (anonymous tool usage) and an opt-in dataset recording. Both need credentials in a `MCP_Server/config.py` file that is **not** part of this repository, so **an install from this repository sends nothing**. Details and switches (`ABLETON_MCP_DISABLE_TELEMETRY`, `ABLETON_MCP_ENABLE_DATASET`) are in [TERMS.md](TERMS.md).

---

## Credits and license

- **Original project:** [ableton-mcp](https://github.com/ahujasid/ableton-mcp) by [Siddharth Ahuja](https://x.com/sidahuj).
- **Extended edition:** Olivier Cedrati ([@cedrati](https://github.com/cedrati)) — mixing and routing, listening and mastering analysis, music theory, clip editing, MIDI import and reliability work. Report issues about this edition on [cedrati/ableton-mcp](https://github.com/cedrati/ableton-mcp/issues).

MIT License — see [LICENSE](LICENSE). This is a third-party integration, not made or endorsed by Ableton.
