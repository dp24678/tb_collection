
function time2DateStr(timestamp) {

    var d = new Date(timestamp);  

    var datestr = (d.getFullYear()) + "-" +

    number((d.getMonth() + 1), 2) + "-" +

    number((d.getDate()), 2) + " " +

    number((d.getHours()), 2) + ":" +

    number((d.getMinutes()), 2) + ":" +

    number((d.getSeconds()), 2);

    return datestr;

}

function number(nums, length) {

    var shuziStr = "";

    if (typeof nums == 'number') {

        shuziStr = "" + nums;

    }

    for (var i = shuziStr.length; i < length; i++) {

        shuziStr = "0" + shuziStr;

    }

    return shuziStr;
}

function isStr(value) {

    if (typeof value == 'string' && value.constructor == String) return true;

    else return false;
}

function getUrlParam(name) {

    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");

    var r = window.location.search.substr(1).match(reg);

    if (r != null) return unescape(r[2]); return null;
}

function getPageBar(curPage, total) {

    var pageStr = "";

    var pageList = 10;//每页显示的页码个数

    var startPage, endPage;

    var totalPage = Math.ceil(total / pageSize);//总页数

    if (pageList > totalPage) {

      pageList = totalPage;

    }

    if (curPage % pageList == 0) {

      startPage = curPage - pageList + 1;

    } else {

      startPage = Math.floor(curPage / pageList) * pageList + 1;

    }

    endPage = ((startPage + pageList) > totalPage) ? totalPage : ((startPage + pageList) - 1);

    //页码小于1
    if (curPage < 1) curPage = 1;

    // pageStr = "<div class='message'>共" + "<i class='blue'>" + total + "</i>" + "条<i>" + curPage + "/" + totalPage + "</i></div>";
    pageStr += "<ul class='pagination'>";

    //首页处理
    // pageStr += "<li class='paginItem'><span class='paginItem'><a href='javascript:void(0)' rel='" + 1 + "'> &lt;&lt;</a></span></li>";
    
    //上一页处理
    if (curPage > 1) {

      pageStr += "<li><a href='javascript:changePage(" + (curPage - 1) + ")' aria-label='上一页' rel=''><span aria-hidden='true'>&laquo;</span></a></li>";
    
    } else {

      pageStr += "<li class='disabled'><a rel='1' href='#' aria-label='上一页'><span aria-hidden='true'>&laquo;</span></a></li>";
    
    }


    for (i = startPage; i <= endPage; i++) {

      //当前页码的样式处理
      if (curPage == i) {

        pageStr += "<li class='active'><a href='#' ref='" + i + "'>" + i + "</a></li>";

      } else {

        pageStr += "<li class=''><a href='javascript:changePage(" + i + ")' ref='" + i + "'>" + i + "</a></li>";

      }

    }
    //if(curPage-spanPage>1){pageStr+="<li class='paginItem'><span class='paginItem'><a href='javascript:void(0)'>...</a></span></li>";}

    //下一页处理
    if (curPage < totalPage) {

      pageStr += "<li><a href='javascript:changePage(" + (parseInt(curPage) + 1) + ")' aria-label='下一页'><span aria-hidden='true'>&raquo;</span></a></li>";
   
    } else {

      pageStr += "<li class='disabled'><a href='#' aria-label='下一页'><span aria-hidden='true'>&raquo;</span></a></li>";

    }
    //尾页处理
    // pageStr += "<li class='paginItem'><span class='paginItem'><a href='javascript:void(0)' rel='" + totalPage + "'>&gt;&gt;</a></span></li>";
    pageStr += "<li class='disabled'><a href='#' aria-label='共" + totalPage + "页/" + total + "条数据'>共" + totalPage + "页/" + total + "条数据</a></li>";


    pageStr += "</ul>";

    $("#pagenav").html(pageStr);

  }

  //去除HTML tag
  function removeHTMLTag(str) {

    str = str.replace(/<\/?[^>]*>/g,''); 

    str = str.replace(/[ | ]*\n/g,'\n'); 

    //str = str.replace(/\n[\s| | ]*\r/g,'\n'); //去除多余空行

    str=str.replace(/&nbsp;/ig,'');//去掉&nbsp;

    return str;
}


function hideModal() {

  $('#myModal').modal('hide');

}

function showModal() {

  $('#myModal').modal({ backdrop: 'static', keyboard: false });

}


function setCookie(name,value)
{
var exp = new Date();
exp.setTime(exp.getTime() + 30*60*1000);
document.cookie = name + "="+ escape (value) + ";expires=" + exp.toGMTString();
}

function getCookie(name)
{
var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
if(arr=document.cookie.match(reg))
return unescape(arr[2]);
else
return null;
}

function delCookie(name)
{
var exp = new Date();
exp.setTime(exp.getTime() - 1);
var cval=getCookie(name);
if(cval!=null)
document.cookie= name + "="+cval+";expires="+exp.toGMTString();
}


function get_uuid() {
    var timestamp = (new Date()).valueOf();  // 当前时间戳，毫秒级
    guid = document.getElementById('guid').valueOf();

    str = guid + timestamp;
    uuid = hex_md5(str);
    return uuid;
}

function set_sort_value() {  // app与pc的排序字段不同，需要根据数据来源更改
    var data_source = document.getElementById('serachType').value;
    console.log(data_source);
    if (data_source == 'APP') {
        document.querySelectorAll('#serachSort option')[0].value = '_mix';  //综合
        document.querySelectorAll('#serachSort option')[1].value = '_sale'; // 销量
        document.querySelectorAll('#serachSort option')[2].value = '_ratesum'; // 信用
        document.querySelectorAll('#serachSort option')[3].value = 'bid'; // 升序
        document.querySelectorAll('#serachSort option')[4].value = '_bid'; // 降序
    }


}


function get_rank_order(data) {
    var data_type = data.search_args.data_sources;
    // alert(data_type);
    // if ( data_type==="APP" ){

    rank_order += data.rank_order;
    return rank_order;
    // }

    // return data.rank_order;
}

