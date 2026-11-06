# ir8tools

A small collection of handy command line utilities bundled together.

## Installation

Requires Python 3. Install the latest version directly from the repository:

```sh
pip install git+https://github.com/rafiibrahim8/ir8tools.git --upgrade
```

Or install in an isolated environment with [pipx](https://pypa.github.io/pipx/):

```sh
pipx install git+https://github.com/rafiibrahim8/ir8tools.git
# Upgrade later with: pipx install --force git+https://github.com/rafiibrahim8/ir8tools.git
```

## Shell completion

Completions are not installed automatically by `pip`/`pipx`. For fish, run once
(and again after upgrading):

```sh
ir8t --completions fish > ~/.config/fish/conf.d/ir8tools.fish
```

This completes options for every tool, tool names after `ir8t`, and the chosen
tool's options after `ir8t <tool>`.

## Usage

Use the launcher to list or run tools:

```sh
# Show available tools
ir8t --list

# Run any tool (pass -h to see its options)
ir8t <tool> [args...]
```

Each tool can also be invoked directly by name, for example `ipinfo -h` or `warpwg -o warp.conf`.

## Available tools

- `ipinfo` – Show information about an IP (no args uses this machine's IP)
- `dnsinfo` – Query DNS records for a domain
- `dnswho` – Display the DNS server currently in use
- `pwned` – Check if a password appears in public breach dictionaries
- `gittu` – Commit and push changes to the current Git branch
- `warpwg` – Generate a WireGuard config for Cloudflare WARP (file or QR)
- `srcf` – Find alternate mirrors for SourceForge downloads
- `base58` – Base58 encode/decode data (same flags as `base64`: `-d`, `-i`, `-w`)
- `echoargs` – Echo the arguments passed (useful for testing)

## Dependencies

Dependencies are installed automatically with `pip`, but the core libraries used are:

- cryptography
- dnspython
- requests
- segno
