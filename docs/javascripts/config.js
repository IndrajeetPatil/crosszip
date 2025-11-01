// Configure dependencies for mkdocs-run-code
// Note: pytest is already available in Pyodide, only install crosszip
window.mkdocs_run_deps = ["crosszip"];

// Ensure run_code initializes after DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log(
    "DOM loaded, code blocks found:",
    document.querySelectorAll(".language-py, .language-python").length
  );
});
