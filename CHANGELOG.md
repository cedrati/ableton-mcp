# Changelog

Changes in this fork ([cedrati/ableton-mcp](https://github.com/cedrati/ableton-mcp), branch `feat/mixer-scenes`) relative to the upstream [ahujasid/ableton-mcp](https://github.com/ahujasid/ableton-mcp).

The version numbers below are the **Remote Script** version (`SCRIPT_VERSION`), which the server checks through `get_remote_script_info`. After updating, reinstall the script with `ableton-mcp-install-script` and **restart Live** — re-selecting the control surface does not reload the code.

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
