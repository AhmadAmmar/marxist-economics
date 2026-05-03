window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    tags: 'ams',
    macros: {
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
      Ts: 'T_{\\mathrm{S}}'
    }
  },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
