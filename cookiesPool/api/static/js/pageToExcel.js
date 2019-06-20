function pageToExcel(jsonData){
          let str = '<tr><td>序号</td><td>位置排名</td><td>图URL</td><td>标题</td><td>是否天猫</td><td>价格</td><td>销量</td><td>收获量</td><td>店铺</td><td>DSR</td><td>信用</td><td>发货地</td></tr>';
          for(let i = 0 ; i < jsonData.length ; i++ ){

              var goods = jsonData[i].goods;

              var shop = jsonData[i].shop;

              var seller = jsonData[i].seller;

              var a = "第"+jsonData[i]['page_order']+"页 总排名：" + jsonData[i]['rank_order'];

              var DSR = "服务" +shop.dsr.service+ "描述"+shop.dsr.description+"物流"+shop.dsr.delivery;
              var order = i + 1;

              let str_ = '<tr><td>'+order+'</td><td>'+a+'</td><td>'+goods.picSrc+'</td><td>'+goods.title+'</td><td>'+goods.is_tmall+'</td><td>'+goods.price+'</td><td>'+goods.sales_count+'</td><td>'+goods.confirm_sales_count+'</td><td>'+shop.name+'</td><td>'+DSR+'</td><td>'+seller.sellerCredit+'</td><td>'+goods.shop_location+'</td></tr>';
              str += str_;
          }
          //Worksheet名
          let worksheet = 'Sheet1';
          // let uri = 'data:application/vnd.ms-excel;base64,';
          let uri = 'data:application/vnd.ms-excel;base64,';

          //下载的表格模板数据
          let template = `<html xmlns:o="urn:schemas-microsoft-com:office:office"
          xmlns:x="urn:schemas-microsoft-com:office:excel"
          xmlns="http://www.w3.org/TR/REC-html40">
          <head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>
            <x:Name>${worksheet}</x:Name>
            <x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet>
            </x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]-->
            </head><body><table>${str}</table></body></html>`;
          //下载模板
          var query  = document.getElementById('tb_search_key').value;
          var a = document.createElement("a");
          a.href = uri + base64(template);
          a.download =query + '.xls';
          a.click();
        }

//输出base64编码
function base64 (s) { return window.btoa(unescape(encodeURIComponent(s))) }