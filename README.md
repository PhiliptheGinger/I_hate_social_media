# I_hate_social_media

This repository currently does **not** contain the old Instagram/Facebook event collector code.
At the moment, the only existing file from earlier work was a privacy policy.

## What this means

If your goal is to find comedy events by mining social media posts, we need to rebuild the collector in small, testable steps.

## Small first step (implemented here)

A lightweight local parser is included at `src/comedy_events.py`.

It does **not** call Instagram/Facebook directly yet. Instead, it:

1. Reads a JSON file of posts you exported or gathered elsewhere.
2. Filters posts that look comedy-related.
3. Tries to infer a location/venue from text.
4. Outputs normalized JSON rows that can later be stored in a DB.

This lets us validate logic before dealing with Meta API auth, permissions, and rate limits.

## Input format

Expected JSON is an array of post objects. Example fields:

```json
[
  {
    "platform": "instagram",
    "text": "Comedy showcase this Friday at The Bell House in Brooklyn 8pm",
    "created_time": "2026-04-20T13:05:00Z",
    "permalink": "https://instagram.com/p/example",
    "location": "Brooklyn, NY"
  }
]
```

Only `text` is required.

## Usage

```bash
python3 src/comedy_events.py \
  --input examples/sample_posts.json \
  --output examples/comedy_events_out.json
```

## Next step after this

Add a real Meta Graph API ingester that writes raw post text into this same schema.
