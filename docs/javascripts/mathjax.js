window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    processEnvironments: true,
    macros: {
      constcap: 'c',
      varcap: 'v',
      surplus: 's',
      profitrate: 'r',
      OCC: '\\Omega',
      exploitrate: 'e',
      organiccomp: '\\Omega',
      MELT: '\\mu',
      Vi: ['V_{#1}', 1],
      LSN: ['L^{\\mathrm{SN}}_{#1}', 1],
      Tn: 'T_{\\mathrm{N}}',
      Ts: 'T_{\\mathrm{S}}',
      CMC: '\\mathrm{C-M-C}',
      MCM: "\\mathrm{M-C-M'}",
      snlt: '\\text{SNLT}',
      profitratefull: '\\text{rate of profit}',
      organiccompfull: '\\text{organic composition of capital}',
      TRPFfull: '\\text{tendency of the rate of profit to fall}'
    }
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
};
