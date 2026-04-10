# =============================================================================
# Makefile -- Pandoc-based build system for
# "Causal Inference: A Pokemon Approach"
# =============================================================================
#
# Usage:
#     make pdf        Build the full textbook as PDF (LaTeX)
#     make html       Build the full textbook as a single HTML page
#     make all        Build everything
#     make clean      Remove build artefacts
#
# Requirements:
#     pandoc, pandoc-citeproc (or pandoc >= 2.11 with --citeproc),
#     a TeX distribution (e.g. TeX Live / MacTeX) with xelatex
# =============================================================================

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
CHAPTER_DIR   := ../../textbook/chapters
BUILD_DIR     := .
OUTPUT_DIR    := $(BUILD_DIR)/output
TEMPLATE_TEX  := $(BUILD_DIR)/template.tex
BIB_FILE      := $(BUILD_DIR)/bibliography.bib
ASSETS_DIR    := ../../assets

# Collect chapter markdown files in order (expects ch01_*.md, ch02_*.md, ...)
CHAPTERS := $(sort $(wildcard $(CHAPTER_DIR)/ch*.md))
APPENDICES := $(sort $(wildcard $(CHAPTER_DIR)/appendix_*.md))
ALL_CONTENT := $(BUILD_DIR)/title.md $(CHAPTERS) $(APPENDICES)
CSS_FILE := $(BUILD_DIR)/textbook.css

# ---------------------------------------------------------------------------
# Output files
# ---------------------------------------------------------------------------
PDF_OUT       := $(OUTPUT_DIR)/causal_inference_pokemon.pdf
HTML_OUT      := $(OUTPUT_DIR)/causal_inference_pokemon.html
WEASY_PDF_OUT := $(OUTPUT_DIR)/causal_inference_pokemon_weasy.pdf
WEASY_HTML    := $(OUTPUT_DIR)/causal_inference_pokemon_for_pdf.html

# ---------------------------------------------------------------------------
# Tool settings
# ---------------------------------------------------------------------------
PANDOC       := pandoc
LATEX_ENGINE := xelatex

# Common Pandoc flags
PANDOC_COMMON := \
	--from=markdown+smart+yaml_metadata_block+citations+footnotes+tex_math_dollars \
	--citeproc \
	--bibliography=$(BIB_FILE) \
	--number-sections \
	--toc \
	--toc-depth=3 \
	--resource-path=$(CHAPTER_DIR):$(ASSETS_DIR)

# PDF-specific flags
PANDOC_PDF := \
	$(PANDOC_COMMON) \
	--pdf-engine=$(LATEX_ENGINE) \
	--template=$(TEMPLATE_TEX) \
	-V documentclass=book \
	-V geometry="margin=1in" \
	-V fontsize=11pt \
	-V colorlinks=true \
	-V linkcolor=KantoRed \
	-V citecolor=KantoBlue \
	-V urlcolor=KantoBlue

# HTML-specific flags
PANDOC_HTML := \
	$(PANDOC_COMMON) \
	--standalone \
	--self-contained \
	--css=https://cdn.jsdelivr.net/npm/water.css@2/out/water.min.css \
	--mathjax \
	--metadata title="Causal Inference: A Pokemon Approach"

# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------
.PHONY: all pdf html weasy release-pdf clean

all: pdf html

pdf: $(PDF_OUT)

html: $(HTML_OUT)

# Weasyprint/Chrome-based PDF build (no LaTeX required)
weasy: $(WEASY_PDF_OUT)

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

$(PDF_OUT): $(CHAPTERS) $(TEMPLATE_TEX) $(BIB_FILE) | $(OUTPUT_DIR)
	@echo "==> Building PDF..."
	$(PANDOC) $(PANDOC_PDF) -o $@ $(CHAPTERS)
	@echo "==> PDF written to $@"

$(HTML_OUT): $(CHAPTERS) $(BIB_FILE) | $(OUTPUT_DIR)
	@echo "==> Building HTML..."
	$(PANDOC) $(PANDOC_HTML) -o $@ $(CHAPTERS)
	@echo "==> HTML written to $@"

# Weasyprint-based PDF: produce a styled single-file HTML, then convert with weasyprint
# Falls back to Chrome headless if weasyprint native libs are not installed.
$(WEASY_HTML): $(CHAPTERS) $(APPENDICES) $(CSS_FILE) $(BUILD_DIR)/title.html | $(OUTPUT_DIR)
	@echo "==> Building styled HTML for PDF..."
	$(PANDOC) \
		--from=markdown+smart+tex_math_dollars+footnotes \
		--standalone --embed-resources \
		--css=$(CSS_FILE) \
		--mathjax \
		--toc --toc-depth=2 \
		--resource-path=.:$(CHAPTER_DIR):$(ASSETS_DIR) \
		--include-before-body=$(BUILD_DIR)/title.html \
		--metadata title="Causal Inference: A Pokemon Approach" \
		-o $@ $(CHAPTERS) $(APPENDICES)

$(WEASY_PDF_OUT): $(WEASY_HTML)
	@echo "==> Converting HTML to PDF..."
	@if command -v weasyprint >/dev/null 2>&1; then \
		echo "  Using weasyprint"; \
		weasyprint $(WEASY_HTML) $(WEASY_PDF_OUT); \
	elif [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then \
		echo "  Using Chrome headless (weasyprint not found)"; \
		"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
			--headless --disable-gpu --no-pdf-header-footer \
			--virtual-time-budget=30000 \
			--print-to-pdf="$$PWD/$(WEASY_PDF_OUT)" \
			"file://$$PWD/$(WEASY_HTML)"; \
	else \
		echo "  ERROR: neither weasyprint nor Chrome headless available"; \
		exit 1; \
	fi
	@echo "==> PDF written to $@"

# Convenience: build the PDF and copy to the release location
release-pdf: $(WEASY_PDF_OUT)
	cp $(WEASY_PDF_OUT) ../Causal_Inference_Pokemon.pdf
	@echo "==> Release PDF: textbook/Causal_Inference_Pokemon.pdf"

clean:
	@echo "==> Cleaning build artefacts..."
	rm -rf $(OUTPUT_DIR)
	@echo "==> Done."
