function pct(value, digits) {
  return (value * 100).toFixed(digits) + '%';
}
function fill(snapshot) {
  const paper = {
    'Sell (losers)': '0.79% (1.56)',
    'Buy (winners)': '1.74% (4.33)',
    'Buy − sell': '0.95% (3.07)',
  };
  const body = document.getElementById('table-body');
  for (const row of snapshot.table) {
    let after = '–';
    let afterDrawdown = '–';
    if (row.net_mean !== undefined) {
      after = pct(row.net_mean, 2) + ' (' + row.net_t.toFixed(2) + ')';
      afterDrawdown = pct(row.net_drawdown, 1);
    }
    const tr = document.createElement('tr');
    const cells = [
      row.portfolio,
      paper[row.portfolio],
      pct(row.gross_mean, 2) + ' (' + row.gross_t.toFixed(2) + ')',
      after,
      pct(row.gross_drawdown, 1),
      afterDrawdown,
    ];
    for (const text of cells) {
      const td = document.createElement('td');
      td.textContent = text;
      tr.appendChild(td);
    }
    body.appendChild(tr);
  }
  document.getElementById('n-periods').textContent = snapshot.table[0].periods;
  document.getElementById('winners-cagr').textContent = pct(snapshot.winners_compound, 1);
  document.getElementById('bench-cagr').textContent = pct(snapshot.benchmark_compound, 1);
  document.getElementById('winners-dd').textContent = pct(snapshot.winners_drawdown, 1);
  const chart = echarts.init(document.getElementById('chart'), null, {renderer: 'svg'});
  chart.setOption({
    textStyle: {fontFamily: '"Times New Roman", Tinos, serif'},
    legend: {itemGap: 28, top: 0},
    tooltip: {trigger: 'axis', axisPointer: {type: 'cross'}},
    grid: {left: 50, right: 20, top: 40, bottom: 30},
    xAxis: {type: 'category', data: snapshot.periods},
    yAxis: {type: 'value', scale: true},
    series: [
      {name: 'Winners decile, after costs', type: 'line', showSymbol: false, color: '#2a78d6', data: snapshot.winners_wealth},
      {name: 'NIFTY 500 (price index)', type: 'line', showSymbol: false, color: '#eb6834', data: snapshot.benchmark_wealth},
    ],
  });
  window.addEventListener('resize', function () { chart.resize(); });
}
fetch('data/snapshot.json').then(function (response) { return response.json(); }).then(fill);
function copyCitation() {
  navigator.clipboard.writeText(document.getElementById('cite-text').textContent);
}
