// Configure dependencies for Pyodide code runner
// Note: pytest is already available in Pyodide, only install crosszip
window.mkdocs_run_deps = ["crosszip"];

// Log debug info about code blocks after DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log(
    "DOM loaded, code blocks found:",
    document.querySelectorAll(".language-py, .language-python").length
  );
});
