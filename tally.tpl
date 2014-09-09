<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<!-- <link href="tally.css" rel=stylesheet type=text/css> -->
<title>Tally</title>

<style type="text/css">
% include( 'tally.css' )
</style>

</head>
<body>

<div class="left">
    <div class="left_box">
        <p><a href="/record">记账啦</a></p>
        <p><a href="/view">查水表</a></p>
    </div>
</div>

<div class="right">

% if operation == 'RECORD' :
    <div class="right_box">
    <p>在下面写上你的花销吧</p>
    <div style="border-bottom: 1px solid #3399FF; width: 300px;"></div>
    
    <p>&nbsp;<font color=red>Table</font></p>
    <form method=post action="insert">
        <table cellspacing=5 style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
    % for i in range( num_of_rows ) :
        <tr>
            <td>商品</td>
            <td><input type=text name=ware{{i}} size=25 value=''></td>
            <td> &nbsp; 费用</td>
            <td><select name=currency{{i}}>
        % for currency in currencies :
                <option {{currency.is_selected}}>{{!currency.html}}
        % end
                </select>
            </td>
            <td><input type=text name=cost{{i}} size=10 value=''></td>
            <td> &nbsp; 备注</td>
            <td><input type=text name=remark{{i}} size=30 value=''> &nbsp;
                <font color=red>msg</font>
            </td>
        </tr>
    % end
        </table>
        <input class="LoginButton" type=submit value=提交>
    </form>
    </div>
% end


% if operation == 'VIEW' :
    <div class="right_box">
    <form method=post action="select">
        <table style="margin-top:10px; margin-bottom: 10px; border: 0px solid #3399FF;">
        <tr>
        <td width=100>选择年月</td>
        <td width=200><select name=year>
            <option selected>2014
            <option>2013
            </select>
            <select name=month>
            <option selected>09/Sept.
            <option>08/Oct.
            <option>07/Jul.
            </select>
        </td>
        <td><input class="LoginButton" type=submit value=查询>
        </tr>
        </table>
    </form>
    
    <div style="border-bottom: 1px solid #3399FF; width: 400px;"></div>
    
    <table class="table_border" style="margin-top:20px;">
        <tr align=center>
            <td width=100>日期</td>
            <td width=50>ID</td>
            <td width=180>商品</td>
            <td width=100>花费</td>
            <td width=160>备忘</td>
        </tr>
<!--        $for pub in arg[0] : -->
            <tr align=center>
            <td width=100>2014-09-07</td>
            <td width=50>1</td>
            <td width=180>a pile of shit</td>
            <td width=100>U.S.$1000</td>
            <td width=160></td>
            </tr>
    </table>
    </div>
% end

</div>
</body>