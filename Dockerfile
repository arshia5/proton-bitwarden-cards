FROM python:3.11-slim

# Install minimal TeX Live needed
# texlive-latex-base: Essential LaTeX
# texlive-latex-recommended: geometry, xcolor, graphics, etc.
# texlive-pictures: tikz/pgf
# texlive-fonts-recommended: helvet (part of standard PS fonts usually, but good to have)
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base \
    texlive-latex-recommended \
    texlive-pictures \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the script and logo images
COPY generate_card.py .
COPY proton-logo.png .
COPY bitwarden-logo.png .
COPY metamask-logo.png .

# Entrypoint allows passing arguments directly
ENTRYPOINT ["python3", "generate_card.py"]
