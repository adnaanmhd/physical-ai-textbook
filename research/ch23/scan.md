# ch23 scan · Formats, storage and data pipelines (scanned 2026-10-06)
## What is new since 2025
- LeRobotDataset v3.0 (Sept 2025): sharded Parquet/MP4, streaming from the Hub, now also HF buckets and a Lance alternative. v2.1-to-v3 converters exist; GR00T still uses v2.
- Robo-DM (ICRA 2025 best-paper finalist): single-file EBML/MKV container; claims up to 70x (lossy) smaller than RLDS and no policy degradation at 75x.
- MCAP remains the ROS 2 default log format; Zarr spec is at v3.1.
## Key primary sources
- LeRobotDataset v3.0 docs — Hugging Face — undated — https://huggingface.co/docs/lerobot/lerobot-dataset-v3 — tech-report — layout, streaming, converter
- LeRobotDataset:v3.0 blog — Capuano et al. — 2025-09-16 — https://huggingface.co/blog/lerobot-datasets-v3 — tech-report — why v3 replaced per-episode files
- MCAP specification — Foxglove — undated, spec version 0 — https://mcap.dev/spec — tech-report — container structure, indexing, compression
- Robo-DM — Chen et al. — 2025-05-21 — https://arxiv.org/abs/2505.15558 — preprint — lossy video compression vs policy performance
- High-Quality, ROS Compatible Video Encoding — Li, Xu, Schwertfeger — 2024-08-01 — https://arxiv.org/abs/2408.00538 — preprint — encoder settings, size versus quality
- RLDS — Ramos et al. — 2021-11-04 — https://arxiv.org/abs/2111.02767 — preprint — TFDS-based episode format
- Zarr core specification v3.1 — Miles et al. — undated — https://zarr-specs.readthedocs.io/en/latest/v3/core/index.html — standard — chunked N-d arrays, codecs
- WebDataset — repository — undated — https://github.com/webdataset/webdataset — tech-report — tar-shard streaming
## Suggested sections
Raw logging (MCAP, ROS 2 bags); training formats compared; video compression and learning; streaming loaders; curation and search; storage tiers and cost; lineage and versioning; lab data-engine case studies.
## Surprises and controversies
- Only Robo-DM gives direct compression-vs-policy evidence; one lab, preprint. Gap: independent study, and primary lab data-engine descriptions (searches returned vendor pages only; not listed).
- Foxglove vendor blogs on MCAP adoption are company claims.
