# Recovery Card Generator (Docker)

A tool to generate a beautiful, physical recovery card PDF for Proton, Bitwarden, and MetaMask without needing to install a full LaTeX distribution locally.

## 🛡️ Security
**IMPORTANT:** Never commit your actual recovery phrases to any repository. This tool is designed to take phrases as command-line arguments or interactive input so they are never saved in the source code.

## 🚀 Usage with Docker

The easiest way to use this is with Docker. It bundles a minimal LaTeX environment.

### 1. Build the image
```bash
docker build -t recovery-card .
```

### 2. Generate your card

**Option A: Save to your current folder**
```bash
docker run --rm -v $(pwd):/output recovery-card \
  --proton "your 12 or 24 word proton phrase" \
  --bitwarden "your-bitwarden-recovery-code" \
  --metamask-phrase "twelve word seed phrase for your metamask wallet" \
  --output /output/my_recovery_card
```

**Option B: Pipe output directly to PDF (Stdout)**
```bash
docker run --rm recovery-card \
  --proton "..." \
  --bitwarden "..." \
  --metamask-phrase "..." \
  --output - > my_recovery_card.pdf
```

### 🛠️ CLI Arguments
- `--proton`: Your Proton recovery phrase.
- `--bitwarden`: Your Bitwarden recovery code.
- `--metamask-phrase`: Your 12-word MetaMask seed phrase.
- `--metamask-account`: (Optional) Account name to display (default: "Main Account").
- `--output`: Output filename (without .pdf) or `-` for binary stdout.

## 🎨 Design
The generator produces a credit-card sized layout with:
- **Proton/Bitwarden Card:** Combined card with brand colors and logos.
- **MetaMask Card:** Dedicated card with a 12-word grid and brand styling.
- **Cutting Guides:** Dashed lines to help you cut the cards to size.

## ⚖️ Privacy
This project runs entirely locally or inside your local Docker container. No data is ever sent to any external server.
