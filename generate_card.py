#!/usr/bin/env python3
"""
Recovery Card Generator
Generates a PDF with Proton, Bitwarden, and MetaMask recovery phrases.
"""

import subprocess
import os
import sys
import argparse

LATEX_TEMPLATE = r"""\documentclass[a4paper,12pt]{article}
\usepackage[margin=0.5in]{geometry}
\usepackage{tikz}
\usetikzlibrary{fadings}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage[T1]{fontenc}
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}

% Define brand colors
\definecolor{protonpurple}{HTML}{6D4AFF}
\definecolor{protonpink}{HTML}{FF6EC7}
\definecolor{cardbase}{HTML}{121219}
\definecolor{cardsurface}{HTML}{1E1E2A}
\definecolor{bitwardenblue}{HTML}{175DDC}
\definecolor{bitwardencyan}{HTML}{00A3FF}
\definecolor{textmuted}{HTML}{8B8B9E}

% MetaMask colors
\definecolor{metamaskOrange}{HTML}{F6851B}
\definecolor{metamaskOrangeDark}{HTML}{E2761B}
\definecolor{metamaskPurple}{HTML}{6B4AC9}
\definecolor{metamaskDark}{HTML}{24292E}
\definecolor{metamaskBg}{HTML}{FAFBFC}

\begin{document}

\pagestyle{empty}
\centering

\vspace*{0.5cm}

% ==================== PROTON + BITWARDEN CARD ====================
\begin{tikzpicture}
    % Main card background
    \fill[cardbase, rounded corners=4mm] (0,0) rectangle (8.56,5.398);
    
    % Subtle glass/frosted overlay effect on top half
    \fill[white, opacity=0.02, rounded corners=4mm] (0,2.7) rectangle (8.56,5.398);
    
    % ==================== PROTON SECTION ====================
    % Proton gradient accent bar
    \shade[left color=protonpurple, right color=protonpink, rounded corners=1.5mm] 
        (0.4,4.85) rectangle (3.2,5.05);
    
    % Proton Logo
    \node[anchor=west] at (0.5,4.35) {
        \includegraphics[height=0.65cm]{proton-logo.png}
    };
    
    % Proton label
    \node[anchor=east, textmuted, font=\tiny\bfseries] at (8.1,4.35) {RECOVERY PHRASE};
    
    % Proton recovery phrase
    \node[anchor=north west, white, font=\fontsize{9}{12}\selectfont\ttfamily, text width=7.6cm, align=left] at (0.5,3.85) {
        <<PROTON_PHRASE>>
    };
    
    % ==================== DIVIDER ====================
    \shade[left color=cardsurface, middle color=textmuted!30, right color=cardsurface] 
        (0.4,2.65) rectangle (8.16,2.67);
    
    % ==================== BITWARDEN SECTION ====================
    % Bitwarden gradient accent bar
    \shade[left color=bitwardenblue, right color=bitwardencyan, rounded corners=1.5mm] 
        (0.4,2.35) rectangle (3.2,2.55);
    
    % Bitwarden Logo
    \node[anchor=west] at (0.5,1.85) {
        \includegraphics[height=0.6cm]{bitwarden-logo.png}
    };
    
    % Bitwarden label
    \node[anchor=east, textmuted, font=\tiny\bfseries] at (8.1,1.85) {RECOVERY CODE};
    
    % Bitwarden recovery phrase
    \node[anchor=north west, white, font=\fontsize{9}{12}\selectfont\ttfamily, text width=7.6cm, align=left] at (0.5,1.35) {
        <<BITWARDEN_PHRASE>>
    };
    
    % ==================== DECORATIVE ELEMENTS ====================
    \fill[protonpurple, opacity=0.15] (7.8,5.398) arc(0:-90:0.76) -- (8.56,5.398) -- cycle;
    \fill[bitwardenblue, opacity=0.15] (0,0.76) arc(180:270:0.76) -- (0,0) -- cycle;

\end{tikzpicture}

\vspace{0.8cm}

% ==================== METAMASK CARD ====================
\begin{tikzpicture}
    % Card background
    \fill[metamaskBg, rounded corners=4mm] (0,0) rectangle (8.56,5.398);
    
    % Orange gradient header
    \shade[top color=metamaskOrange, bottom color=metamaskOrangeDark, rounded corners=4mm] 
        (0,4.6) rectangle (8.56,5.398);
    \fill[metamaskOrange] (0,4.6) rectangle (8.56,4.9);
    
    % MetaMask Logo
    \node[anchor=west] at (0.4,5.0) {
        \includegraphics[height=0.55cm]{metamask-logo.png}
    };
    
    % Title in header
    \node[white, font=\large\bfseries, anchor=west] at (1.1,5.0) {MetaMask};
    
    % Seed phrase label
    \node[anchor=east, metamaskPurple, font=\tiny\bfseries] at (8.1,5.0) {SECRET RECOVERY PHRASE};
    
    % Account name
    \node[metamaskPurple, font=\small\bfseries, anchor=west] at (0.4,4.25) {<<METAMASK_ACCOUNT>>};
    
    % 12-word seed phrase grid (3 rows x 4 columns)
    % Row 1 (words 1-4)
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (0.4,3.25) {1.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (0.75,3.25) {<<WORD1>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (2.5,3.25) {2.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (2.85,3.25) {<<WORD2>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (4.6,3.25) {3.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (4.95,3.25) {<<WORD3>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (6.7,3.25) {4.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (7.05,3.25) {<<WORD4>>};
    
    % Row 2 (words 5-8)
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (0.4,2.15) {5.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (0.75,2.15) {<<WORD5>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (2.5,2.15) {6.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (2.85,2.15) {<<WORD6>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (4.6,2.15) {7.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (4.95,2.15) {<<WORD7>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (6.7,2.15) {8.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (7.05,2.15) {<<WORD8>>};
    
    % Row 3 (words 9-12)
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (0.4,1.05) {9.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (0.75,1.05) {<<WORD9>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (2.5,1.05) {10.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (2.95,1.05) {<<WORD10>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (4.6,1.05) {11.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (5.05,1.05) {<<WORD11>>};
    
    \node[metamaskOrange, font=\scriptsize\bfseries, anchor=west] at (6.7,1.05) {12.};
    \node[metamaskDark, font=\footnotesize\ttfamily, anchor=west] at (7.15,1.05) {<<WORD12>>};
    
    
    % Border
    \draw[metamaskOrange, rounded corners=4mm, line width=0.4mm] (0,0) rectangle (8.56,5.398);

\end{tikzpicture}

\vspace{0.8cm}

\end{document}
"""


def format_proton_phrase(phrase: str) -> str:
    """Format Proton phrase with proper spacing for two lines."""
    words = phrase.strip().split()
    if len(words) <= 6:
        return r"\hspace{0.5em}".join(words)
    
    # Split into two lines
    mid = len(words) // 2
    line1 = r"\hspace{0.5em}".join(words[:mid])
    line2 = r"\hspace{0.5em}".join(words[mid:])
    return f"{line1}\\\\[4pt]\n        {line2}"


def generate_card(proton_phrase: str, bitwarden_phrase: str, 
                  metamask_phrase: str, metamask_account: str,
                  output_name: str = "recovery_cards"):
    """Generate the PDF card with the given phrases."""
    
    # Format the phrases
    formatted_proton = format_proton_phrase(proton_phrase)
    formatted_bitwarden = bitwarden_phrase.strip()
    
    # Parse MetaMask 12-word phrase
    metamask_words = metamask_phrase.strip().split()
    if len(metamask_words) != 12:
        print(f"⚠ Warning: MetaMask phrase has {len(metamask_words)} words (expected 12)")
        # Pad with empty strings if needed
        while len(metamask_words) < 12:
            metamask_words.append("???")
    
    # Replace placeholders in template
    latex_content = LATEX_TEMPLATE.replace("<<PROTON_PHRASE>>", formatted_proton)
    latex_content = latex_content.replace("<<BITWARDEN_PHRASE>>", formatted_bitwarden)
    latex_content = latex_content.replace("<<METAMASK_ACCOUNT>>", metamask_account)
    # latex_content = latex_content.replace("<<WALLET_ADDRESS>>", wallet_address) # Removed

    
    # Replace MetaMask words
    for i, word in enumerate(metamask_words[:12], 1):
        latex_content = latex_content.replace(f"<<WORD{i}>>", word)
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Handle output path
    if output_name == "-":
        # Temporary file for stdout mode
        import tempfile
        temp_dir = tempfile.mkdtemp()
        work_dir = temp_dir
        tex_file = os.path.join(work_dir, "card.tex")
        job_name = "card"
    else:
        work_dir = script_dir
        if os.path.isabs(output_name):
             # If absolute path, we need to handle directory and filename
             work_dir = os.path.dirname(output_name)
             job_name = os.path.splitext(os.path.basename(output_name))[0]
        else:
             job_name = output_name
             
        tex_file = os.path.join(work_dir, f"{job_name}.tex")

    # Write the LaTeX file
    with open(tex_file, "w") as f:
        f.write(latex_content)
    
    if output_name != "-":
        print(f"✓ Generated {tex_file}", file=sys.stderr)
    
    # Compile to PDF
    if output_name != "-":
        print("⏳ Compiling PDF...", file=sys.stderr)
        
    try:
        # pdflatex needs to run in the directory where images are if we use relative paths for images
        # But we are in script_dir usually. The images are in script_dir.
        # If we run in temp_dir, we need access to images.
        # Let's run in script_dir and specify output-directory if possible or just move result.
        
        # If writing to stdout, we use a temp dir but need images.
        # Images are used as relative paths in LATEX_TEMPLATE: \includegraphics{proton-logo.png}
        # latex command runs in cwd.
        
        cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={work_dir}", tex_file]
        
        # If using temp dir, we need to symlink images or run in script dir but write to temp dir
        if output_name == "-":
             cmd = ["pdflatex", "-interaction=nonstopmode", f"-output-directory={work_dir}", tex_file]
             # We should run this from script_dir so it finds images
        
        result = subprocess.run(
            cmd,
            cwd=script_dir,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            pdf_file = os.path.join(work_dir, f"{job_name}.pdf")
            
            if output_name == "-":
                with open(pdf_file, "rb") as f:
                    sys.stdout.buffer.write(f.read())
            else:
                print(f"✓ Generated {pdf_file}", file=sys.stderr)
            
            # Clean up auxiliary files
            generated_files = [f"{job_name}{ext}" for ext in [".aux", ".log", ".fls", ".fdb_latexmk", ".synctex.gz", ".tex", ".pdf"]]
            
            if output_name != "-":
                # Keep pdf and tex if not stdout
                cleanup_exts = [".aux", ".log", ".fls", ".fdb_latexmk", ".synctex.gz"]
                for ext in cleanup_exts:
                    aux_file = os.path.join(work_dir, f"{job_name}{ext}")
                    if os.path.exists(aux_file):
                        os.remove(aux_file)
                print("✓ Cleaned up auxiliary files", file=sys.stderr)
            else:
                # Cleanup everything in temp dir
                import shutil
                shutil.rmtree(work_dir)

        else:
            print("✗ PDF compilation failed:", file=sys.stderr)
            print(result.stdout, file=sys.stderr)
            print(result.stderr, file=sys.stderr)
            sys.exit(1)
            
    except FileNotFoundError:
        print("✗ pdflatex not found. Please install a LaTeX distribution (e.g., MacTeX, TeX Live)", file=sys.stderr)
        if output_name != "-":
            print(f"  The .tex file has been generated at: {tex_file}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Generate recovery card PDF")
    parser.add_argument("--proton", help="Proton recovery phrase")
    parser.add_argument("--bitwarden", help="Bitwarden recovery code")
    parser.add_argument("--metamask-phrase", help="MetaMask 12-word seed phrase")
    parser.add_argument("--metamask-account", default="Main Account", help="MetaMask account name")
    parser.add_argument("--output", default="recovery_cards", help="Output filename (without extension) or '-' for stdout")
    
    args = parser.parse_args()
    
    # If standard args are provided, use them
    if args.proton or args.bitwarden or args.metamask_phrase:
        if not (args.proton and args.bitwarden and args.metamask_phrase):
             print("Error: If using CLI arguments, --proton, --bitwarden and --metamask-phrase are required.", file=sys.stderr)
             sys.exit(1)
             
        proton_phrase = args.proton
        bitwarden_phrase = args.bitwarden
        metamask_phrase = args.metamask_phrase
        metamask_account = args.metamask_account
        output_name = args.output
        
        generate_card(proton_phrase, bitwarden_phrase, metamask_phrase, metamask_account, output_name)
        return

    # Interactive mode (backward compatibility)
    print("=" * 50)
    print("  Recovery Card Generator")
    print("=" * 50)
    print()
    
    # Get Proton phrase
    print("Enter your Proton recovery phrase (12 or 24 words):")
    proton_phrase = input("> ").strip()
    
    if not proton_phrase:
        print("✗ Proton phrase cannot be empty")
        sys.exit(1)
    
    print()
    
    # Get Bitwarden phrase
    print("Enter your Bitwarden recovery code:")
    bitwarden_phrase = input("> ").strip()
    
    if not bitwarden_phrase:
        print("✗ Bitwarden phrase cannot be empty")
        sys.exit(1)
    
    print()
    
    # Get MetaMask info
    print("Enter your MetaMask account name (e.g., Main Account):")
    metamask_account = input("> ").strip() or "Main Account"
    
    print()
    
    print("Enter your MetaMask 12-word seed phrase:")
    metamask_phrase = input("> ").strip()
    
    if not metamask_phrase:
        print("✗ MetaMask phrase cannot be empty")
        sys.exit(1)
    
    
    print()
    
    # print("Enter your MetaMask wallet address (0x...):")
    # wallet_address = input("> ").strip() or "0x0000000000000000000000000000000000000000"
    
    # print()
    
    # Generate the card
    generate_card(proton_phrase, bitwarden_phrase, metamask_phrase, metamask_account)
    
    print()
    print("🎉 Done! Your recovery cards are ready to print.")


if __name__ == "__main__":
    main()
