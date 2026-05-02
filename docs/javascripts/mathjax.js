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
      snlt: '\\text{SNLT}',
      profitratefull: '\\text{rate of profit}',
      organiccompfull: '\\text{organic composition of capital}',
      TRPFfull: '\\text{tendency of the rate of profit to fall}'
    }
  },
  options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }
};
