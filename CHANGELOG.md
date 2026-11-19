# Changelog

Changes in this fork ([cedrati/ableton-mcp](https://github.com/cedrati/ableton-mcp), branch `feat/mixer-scenes`) relative to the upstream [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp).

The version numbers below are the **Remote Script** version (`SCRIPT_VERSION`), which the server checks through `get_remote_script_info`. After updating, reinstall the script with `ableton-mcp-install-script` and **restart Live** — re-selecting the control surface does not reload the code.

## Remote Script 1.9.0

### Added

New MCP tools and matching Remote Script commands. Each takes `location`: `session` (clip slot index) or `arrangement` (index as listed by `get_arrangement_clips`).

- **Warp:** `get_clip_warp`, `set_clip_warp` (warping, warp mode, pitch, gain), `edit_warp_markers` (Live 11+). `set_clip_warp(original_bpm=…)` conforms a loop to the song tempo: it turns warping on, keeps the first warp marker and pins the last whole beat of the file to its time at that tempo.
- **Clip automation:** `set_clip_automation` writes a clip envelope for a device parameter or a mixer control (volume, panning, sends), from points with linear ramps or held steps; an empty point list clears it. `get_clip_automation` samples an envelope back. Session clips only: Live 12 refuses clip automation on Arrangement clips from a script, and Arrangement automation lanes aren't reachable from its API.

### Internal

- `_resolve_clip()` resolves Session and Arrangement clips for the new commands.
- New tests in `tests/test_warp_automation.py` (fake Clip / AutomationEnvelope).

## Remote Script 1.8.2

### Fixed

- **Error messages:** refusals from Live (out-of-range index, master track can't be muted…) are no longer prefixed with `Communication error with Ableton:`, which suggested a connection problem. The server also keeps the socket open after such a refusal instead of dropping it and reconnecting. Real transport failures (timeout, lost connection, invalid response) are reported as before.
- **Master track name:** `get_session_info` reported the master as `"Master"` (hardcoded) while the mixer tools reported Live's actual name (`"Main"` in Live 12). It now reads the name from Live.

## Remote Script 1.8.1

### Fixed

Live applies some changes asynchronously: reading the state back right after a write returns the old value. Three commands were affected.

- **`set_arrangement_time`** reported the previous playhead position (e.g. asked for beat 16, replied "0.0"). It now replies once Live reports the playhead at the requested beat.
- **`create_locator`** failed with "Failed to create cue" unless the playhead was already at the target beat, because the cue was toggled at the old playhead position. It now waits for the playhead to arrive, creates the cue, waits for it to appear, names it, and restores the playhead. It now refuses to run while the transport is playing instead of misplacing the cue.
- **`load_instrument_or_effect`** replied "Devices on track:" with an empty list: the device chain was read before Live inserted the device, and the `new_devices` / `devices_after` fields the server expects were never sent. The reply now lists the new device(s). Loading the same device that is already on the track is detected as an in-place reload (Live keeps the device and resets its parameters).

When Live hasn't applied the change within the wait budget (1 s for the playhead, 5 s for a device load, 2 s for an in-place reload), the reply says so instead of reporting stale state.

### Internal

- Commands can now complete over several Live ticks (`_Deferred` + `_poll_until` in the Remote Script).
- New regression tests (`tests/test_async_live_state.py`) simulate Live applying writes one tick later.

## Remote Script 1.8.0

### Added

New MCP tools and matching Remote Script commands:

- **Mixer:** `set_track_volume`, `set_track_panning`, `set_track_send`, `set_track_mute`, `set_track_solo`, `set_track_arm` — on regular tracks, and (where it applies) return tracks and the master via `track_type`.
- **Tracks:** `duplicate_track`, `delete_track`.
- **Scenes:** `get_scenes`, `create_scene`, `set_scene_name`, `duplicate_scene`, `fire_scene`, `delete_scene`.
- **Arrangement:** `delete_arrangement_clip` (Live 11+).

See the [tool reference](README.md#tools-added-by-this-fork) for parameters.
