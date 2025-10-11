// Configure dependencies for mkdocs-run-code
window.mkdocs_run_deps = ["pytest", "crosszip"];

// Ensure run_code initializes after DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  console.log(
    "DOM loaded, code blocks found:",
    document.querySelectorAll(".language-py, .language-python").length
  );
});
