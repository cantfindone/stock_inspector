window.onload = function () {
//
//      document.writeln("<ul class=\'menu\' id=\'menu\'>");
//      document.writeln("    <li><span>复制</span></li>");
//      document.writeln("    <li><span>粘贴</span></li>");
//      document.writeln("    <li><span>刷新</span></li>");
//      document.writeln("    <li><span>其他功能1</span></li>");
//      document.writeln("    <li><span>其他功能2</span></li>");
//      document.writeln("  </ul>");
      // 获取节点
      var menu = document.getElementById('menu');

      //获取可视区宽度,高度
      var winWidth = document.documentElement.clientWidth || document.body.clientWidth;
      var winHeight = document.documentElement.clientHeight || document.body.clientHeight;

      // 点击空白区域 隐藏菜单
      document.addEventListener('click', function () {
        menu.style.display = 'none';
        menu.style.left = 0 + 'px';
        menu.style.top = 0 + 'px';
      })

      // 点击菜单
      menu.addEventListener('click', function (e) {
        var e = e || window.event;
        console.log(e.target.innerText)
      })

      //右键菜单
      document.oncontextmenu = function (e) {
        var e = e || window.event;
        row = e.path[1].innerHTML.match("<th>\\d+</th>\\s+<td>(\\d+)</td>\\s+<td>(\\S+)</td>")
        console.log(RegExp.$1)
        console.log(RegExp.$2)
        window.stock_code=RegExp.$1
        window.stock_name=RegExp.$2
        menu.style.display = 'block';
        // 获取鼠标坐标
        var mouseX = e.clientX;
        var mouseY = e.clientY;

        // 判断边界值，防止菜单栏溢出可视窗口
        if (mouseX >= (winWidth - menu.offsetWidth)) {
          mouseX = winWidth - menu.offsetWidth;
        } else {
          mouseX = mouseX
        }
        if (mouseY > winHeight - menu.offsetHeight) {
          mouseY = winHeight - menu.offsetHeight;
        } else {
          mouseY = mouseY;
        }
        menu.style.left = mouseX + 'px';
        menu.style.top = mouseY-20 + 'px';
        return false;
      }
    }


function getSelect() {
  "" == (window.getSelection ? window.getSelection() : document.selection.createRange().text) ? alert("请选择需要复制的内容！") : document.execCommand("Copy")
}
function stock_indicator() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/stock_indicator")
}

function stock_indicator_plot() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/stock_indicator_plot")
}
function finance_indicator_plot() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/finance_indicator_plot")
}
function balance() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/balance")
}

function balance_plot() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/balance_plot")
}
function cash() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/cash")
}

function cash_plot() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/cash_plot")
}
function income() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/income")
}

function income_plot() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/income_plot")
}
function zygc() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/zygc")
}

function zygc_plot() {
  var a = window.getSelection ? window.getSelection() : document.selection.createRange().text;
  window.open("/stock/" + window.stock_code+ "/" +window.stock_name +"/zygc_plot")
}