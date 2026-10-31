window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],  // the Markdown step has already marked all maths, so a $ in text is money
    displayMath: [['\\[', '\\]']],
    processEscapes: true,
    tags: 'ams',
    packages: {'[+]': ['html']},
    macros: {
      ensuremath: ['#1', 1],
      pounds: '\\unicode{xA3}',
      euro: '\\unicode{x20AC}',
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
