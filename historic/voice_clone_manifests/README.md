# Original Voice Clone Manifests

This folder contains copied manifest CSV files from:

```text
/Users/xieyulong2022/AI_Learn/Codex/voice_clone/output/
```

These files are historical references. They record prior short-segment batch
metadata such as scene IDs, clip names, timeline targets, generated durations,
narration text, subtitle text, and relative output paths.

Use them to:

- compare planned time slots against actual generated durations;
- understand prior short-segment batch structure;
- design migration from row-level WAV clips to scene-level long WAV files;
- preserve timing evidence without copying old generated media.

Do not treat these files as current output manifests for the new long-scene
workflow. New manifests should be written under:

```text
output/manifests/
```

Copied audio and caption paths inside these historic manifests are relative
paths from the old project and are not expected to exist in this repository.
