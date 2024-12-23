# Makefile for building Sphinx documentation

# The source directory of your docs
SRC_DIR = docs/source

# The build directory for the output
BUILD_DIR = build

# The output format you want (can be html, latex, etc.)
OUTPUT_FORMAT = html

# Sphinx build command
SPHINX_BUILD = sphinx-build

# Sphinx source and build directories
SPHINX_SOURCE = $(SRC_DIR)
SPHINX_BUILD_DIR = $(BUILD_DIR)/$(OUTPUT_FORMAT)

# Sphinx options
SPHINX_OPTIONS = -v

# The target html builds the documentation in HTML format
html: $(SPHINX_BUILD_DIR)

# Target to build the HTML docs
$(SPHINX_BUILD_DIR):
	@echo "Building documentation..."
	$(SPHINX_BUILD) $(SPHINX_OPTIONS) $(SPHINX_SOURCE) $(SPHINX_BUILD_DIR)

# Clean up build directory (useful for removing old builds)
clean:
	@echo "Cleaning build directory..."
	rm -rf $(BUILD_DIR)

# Rebuild the documentation (clean + build)
rebuild: clean html

# Target to serve documentation locally using Python's built-in server
serve: html
	@echo "Serving documentation at http://localhost:8000"
	python3 -m http.server --directory $(SPHINX_BUILD_DIR) 8000

# Help command to show available targets
help:
	@echo "Available commands:"
	@echo "  html       - Build the documentation in HTML format"
	@echo "  clean      - Remove build files"
	@echo "  rebuild    - Clean and then build"
	@echo "  serve      - Serve documentation locally"
	@echo "  help       - Show this message"
