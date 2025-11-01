/**
 * Pyodide-based code runner for MkDocs
 * Enables interactive Python code execution in the browser
 */

class PyodideRunner {
  constructor() {
    this.pyodide = null;
    this.loading = false;
    this.loaded = false;
    this.loadPromise = null;
  }

  /**
   * Load Pyodide and initialize it
   */
  async loadPyodide() {
    if (this.loaded) return this.pyodide;
    if (this.loading) return this.loadPromise;

    this.loading = true;
    this.loadPromise = (async () => {
      try {
        // Load Pyodide from CDN
        const script = document.createElement("script");
        script.src = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
        document.head.appendChild(script);

        await new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = reject;
        });

        // Initialize Pyodide
        this.pyodide = await loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/",
        });

        // Load micropip for package installation
        await this.pyodide.loadPackage("micropip");

        this.loaded = true;
        this.loading = false;
        return this.pyodide;
      } catch (error) {
        this.loading = false;
        throw new Error(`Failed to load Pyodide: ${error.message}`);
      }
    })();

    return this.loadPromise;
  }

  /**
   * Install Python packages using micropip
   */
  async installPackages(packages) {
    const pyodide = await this.loadPyodide();
    const micropip = pyodide.pyimport("micropip");

    for (const pkg of packages) {
      try {
        await micropip.install(pkg);
      } catch (error) {
        console.warn(`Failed to install package ${pkg}:`, error);
      }
    }
  }

  /**
   * Execute Python code
   */
  async runCode(code, packages = []) {
    const pyodide = await this.loadPyodide();

    // Install packages if needed
    if (packages.length > 0) {
      await this.installPackages(packages);
    }

    // Capture stdout
    const output = [];
    pyodide.setStdout({
      batched: (text) => output.push(text),
    });

    try {
      // Run the code
      await pyodide.runPythonAsync(code);
      return {
        success: true,
        output: output.join(""),
        error: null,
      };
    } catch (error) {
      return {
        success: false,
        output: output.join(""),
        error: error.message,
      };
    }
  }
}

// Global instance
window.pyodideRunner = new PyodideRunner();

/**
 * Interactive code block handler
 */
class InteractiveCodeBlock {
  constructor(element) {
    this.element = element;
    this.code = this.extractCode();
    // Mark element as Pyodide-enabled for CSS styling
    element.classList.add("pyodide-enabled");
    this.setupUI();
  }

  extractCode() {
    const codeElement = this.element.querySelector("code");
    return codeElement ? codeElement.textContent : "";
  }

  setupUI() {
    // Create container for buttons and output
    const container = document.createElement("div");
    container.className = "pyodide-controls";

    // Run button
    const runButton = document.createElement("button");
    runButton.className = "pyodide-run-btn";
    runButton.textContent = "▶ Run";
    runButton.onclick = () => this.runCode();

    // Clear button
    const clearButton = document.createElement("button");
    clearButton.className = "pyodide-clear-btn";
    clearButton.textContent = "⎚ Clear";
    clearButton.onclick = () => this.clearOutput();
    clearButton.style.display = "none";

    container.appendChild(runButton);
    container.appendChild(clearButton);

    // Create output div (hidden initially)
    const outputDiv = document.createElement("div");
    outputDiv.className = "pyodide-output";
    outputDiv.style.display = "none";

    // Insert controls and output after the code block
    this.element.parentNode.insertBefore(container, this.element.nextSibling);
    container.after(outputDiv);

    // Store references
    this.runButton = runButton;
    this.clearButton = clearButton;
    this.container = container;
    this.outputDiv = outputDiv;
  }

  async runCode() {
    // Disable button during execution
    this.runButton.disabled = true;
    this.runButton.textContent = "⏳ Running...";

    // Clear previous output content
    this.outputDiv.innerHTML = "";
    this.outputDiv.style.display = "block";

    try {
      // Show loading message
      this.outputDiv.innerHTML = '<div class="pyodide-loading">Loading Python environment...</div>';

      // Get packages from config (if available)
      const packages = window.mkdocs_run_deps || ["pytest", "crosszip"];

      // Run the code
      const result = await window.pyodideRunner.runCode(this.code, packages);

      // Display output
      if (result.success) {
        if (result.output) {
          this.outputDiv.innerHTML = `<pre class="pyodide-stdout">${this.escapeHtml(result.output)}</pre>`;
        } else {
          this.outputDiv.innerHTML = '<div class="pyodide-success">✓ Code executed successfully (no output)</div>';
        }
      } else {
        this.outputDiv.innerHTML = `<pre class="pyodide-error">Error: ${this.escapeHtml(result.error)}</pre>`;
      }

      // Show clear button
      this.clearButton.style.display = "inline-block";
    } catch (error) {
      this.outputDiv.innerHTML = `<pre class="pyodide-error">Failed to execute: ${this.escapeHtml(error.message)}</pre>`;
      this.clearButton.style.display = "inline-block";
    } finally {
      // Re-enable button
      this.runButton.disabled = false;
      this.runButton.textContent = "▶ Run";
    }
  }

  clearOutput() {
    if (this.outputDiv) {
      this.outputDiv.innerHTML = "";
      this.outputDiv.style.display = "none";
    }
    this.clearButton.style.display = "none";
  }

  escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}

/**
 * Track processed code blocks to avoid duplicate initialization
 */
const processedBlocks = new WeakSet();

/**
 * Initialize interactive code blocks
 */
function initPyodideCodeBlocks() {
  // Find all Python code blocks
  const codeBlocks = document.querySelectorAll(
    ".language-python, .language-py"
  );

  codeBlocks.forEach((block) => {
    const codeElement = block.querySelector("code");
    if (codeElement) {
      const code = codeElement.textContent;
      // Check if code has a special marker comment for Pyodide
      if (code.includes("# @pyodide") || block.classList.contains("pyodide")) {
        const highlightContainer = block.closest(".highlight");
        // Only process if container exists and hasn't been processed
        if (highlightContainer && !processedBlocks.has(highlightContainer)) {
          processedBlocks.add(highlightContainer);
          new InteractiveCodeBlock(highlightContainer);
        }
      }
    }
  });
}

// Initialize when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initPyodideCodeBlocks);
} else {
  initPyodideCodeBlocks();
}

// Also re-initialize when instant loading occurs (MkDocs Material feature)
// Debounce to avoid excessive processing
let debounceTimer;
document.addEventListener("DOMContentLoaded", () => {
  const observer = new MutationObserver(() => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      initPyodideCodeBlocks();
    }, 250); // Debounce for 250ms
  });
  observer.observe(document.body, { childList: true, subtree: true });
});
