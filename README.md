# pancalc-registry

> The official add-in registry for [PanCalc Tools](https://github.com/pan-devs/pancalc-tools) — a package manager and developer toolkit for the Casio fx-CG50 and fx-CG100.

---

## Structure

```
pancalc-registry/
├── registry.json        ← index of all add-ins
├── addins/              ← one JSON per add-in
│   ├── utilities.json
│   ├── khicas.json
│   ├── nesizm.json
│   └── ...
├── pandevs.asc          ← Pan Devs public GPG key
└── CONTRIBUTING.md      ← how to submit an add-in
```

## Usage

This registry is consumed automatically by `pcalc`. You don't need to interact with it directly.

```bash
pcalc list              # browse all add-ins
pcalc search <query>    # search by name or tag
pcalc info <id>         # full details
pcalc install <id>      # install to your calculator
```

## Contributing

Want to add an add-in? See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Verification

All approved add-ins are signed with the Pan Devs GPG key (`1A370E1B68A194A8`).  
Public key: [`pandevs.asc`](./pandevs.asc) — also on [keys.openpgp.org](https://keys.openpgp.org/search?q=pan.devs%40proton.me)

---

Maintained by [Pan Devs](https://github.com/pan-devs)
