window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    tags: 'ams',
    packages: {'[+]': ['html']},
    macros: {
      ensuremath: ['#1', 1],
      constcap: 'c',
      varcap: 'v',
      surplus: 's',
      profitrate: 'r',
      exploitrate: 'e',
      OCC: '\\mathrm{OCC}',
      organiccomp: '\\mathrm{OCC}',
      TRPF: '\\mathrm{TRPF}',
      MELT: '\\mu',
      Tn: 'T_{\\mathrm{N}}',
      Ts: 'T_{\\mathrm{S}}',
      LSN: ['L^{\\mathrm{SN}}_{#1}', 1],
      Vi: ['V_{#1}', 1]
    }
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
};
