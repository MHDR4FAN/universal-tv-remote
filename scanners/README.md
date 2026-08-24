# Scanner backends

Each brand can have its own discovery implementation here.

- `lg`: currently uses `lgtvremote-cli scan`.
- Samsung, Sony, Philips, Panasonic and Toshiba are intentionally isolated for platform-specific discovery.

Do not assume that every TV from a brand uses the same protocol; model/platform detection should be added as backends mature.
