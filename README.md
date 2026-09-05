# pancalc-registry

> The official add-in and game registry for [PanCalc Tools](https://github.com/pan-devs/pancalc-tools) — a package manager and developer toolkit for the Casio fx-CG50 and fx-CG100.

---

## Structure

```
pancalc-registry/
├── registry.json        ← index of all add-ins + games
├── addins/              ← one JSON per add-in
│   ├── utilities.json
│   ├── khicas.json
│   ├── nesizm.json
│   └── ...
├── games/               ← one JSON per emulator game
│   └── test_rom.json    ← mock/test entry (do not download — not a real game)
├── files/               ← hosted add-in files and GPG signatures
├── tools/               ← helper scripts for contributors
├── pandevs.asc          ← Pan Devs public GPG key
└── CONTRIBUTING.md      ← how to submit an add-in or game
```

## Usage

This registry is consumed automatically by `pcalc`. You don't need to interact with it directly.

```bash
pcalc list              # browse all add-ins + games
pcalc search <query>    # search by name or tag
pcalc info <id>         # full details
pcalc install <id>      # install to your calculator
pcalc games list        # browse games only
pcalc games install <id> # install a game ROM
```

## Contributing

Want to add an add-in or game? See [CONTRIBUTING.md](./CONTRIBUTING.md).

> - To understand the code or doubts, ask this chatbot https://deepwiki.com/pan-devs/pancalc-registry
> - Use the interactive helper: `python tools/make_addin.py`

## Verification

All approved add-ins are signed with the Pan Devs GPG key (`1A370E1B68A194A8`).  
Public key: [`pandevs.asc`](./pandevs.asc) — also on [keys.openpgp.org](https://keys.openpgp.org/search?q=pan.devs%40proton.me)

Game ROM files are verified by SHA256 only (no PGP).

## AI Assistance

The idea and design are the author's own. The code implementation is supported
by, and in large part written with, AI assistance.


---

Maintained by [Pan Devs](https://github.com/pan-devs)
